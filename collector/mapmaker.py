#!/usr/bin/env python
# encoding: utf-8
"""
mapmaker.py

Created by Maksim Tsvetovat on 2011-12-19.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import simplejson as json
from collections import defaultdict
import candidates as can
import logging
import bsddb
import csv
import s3writer
import settings

l=logging.getLogger("MAP_MAKER")

class mapmaker(object):
    """MapMaker is a class that generates county-by-county maps from tweets"""
    
    def __init__(self, interval=10): 
        self.s3=s3writer.s3writer()
        self.db=self._read_ziptable()
        
        self.count=0
        self.interval=interval
        self.zip_can={}
        ## check for existing files -- maybe we crashed and need to recover?
        self._read_data(from_s3=False, from_file=True)
        
        ## Initialize the zip-to-county table from a CSV file. 
        
        
            
    ### read the csv file 
    def _read_ziptable(self,filename='zip2county.csv'):
        """Read a translation table zipcode -> county code"""
        db={}
        for row in csv.reader(open(settings.geoPath+filename,'rU')):
            db[row[0]]=row[1]
        return db
        
            
    def _intersect(self, a, b):
        """intersect 2 lists and return the result"""
        return list(set(a) & set(b))
         
    def add_to_map(self, location, tokens):
        self.count+=1
        for key in can.candidates.keys():
            try:
                zzip=location['uzip']
            except KeyError:
                return
                
            if zzip !='' and zzip is not None:
                try :
                    county=self.db[zzip]
                except KeyError: 
                    return
                    
                #print zzip, county
                
                if self._intersect(tokens,can.candidates[key]) != []:
                    if county in self.zip_can[key]:
                        self.zip_can[key][county]+=1
                    else:
                        self.zip_can[key][county]=1
                    
        ##if it's been a while since the last write, do a write now, and resent counter
        if self.count >= self.interval:
            #self._dump()
            self._write_data()
            self.count=0            
                    
    def _dump(self):
        """Write out map data as JSON files"""
        l.info(">>>>Writing out choropleths")
        f=settings.jsonPath+"zipmap_"
        for key in self.zip_can.keys():
            out=open(f+key+".json",'wb')
            out.write(json.dumps(self.zip_can[key]))

    def _read_data(self, from_s3=False, from_file=True):
        """reads and initializes the tables; switch s3 to True to read from S3, file to True to read from local files; only one can be set at a time"""

        l.info("Initializing MapMaker")
        if from_s3:
            f=.json
            for key in can.candidates.keys():
                data=self.s3.read(f+key+".json")
                self.zip_can[key]=json.loads(data)
        if from_file:
            f=settings.jsonPath+"zipmap_"
            for key in can.candidates.keys():
             try :
                 out=open(f+key+".json",'rb')
                 self.zip_can[key]=json.loads(out.read())           
             except IOError:            
                 self.zip_can[key]={}        

    def _write_data(self, to_s3=True, to_file=True):
        """Write out map data as JSON files to S3, to a local file OR BOTH"""
        l.info(">>>>Writing out choropleths")
        if to_file:
            f=settings.jsonPath+"zipmap_"
            for key in self.zip_can.keys():
                out=open(f+key+".json",'wb')
                out.write(json.dumps(self.zip_can[key]))
        if to_s3:
            f="zipmap_"
            for key in self.zip_can.keys():
                self.s3.write(f+key+".json", json.dumps(self.zip_can[key]))
            
    def test(self):
        infile=open(settings.jsonPath+"test_output.json")
        for line in infile:
            js=json.loads(line)
            tokens=js['tokens']
            geo=js['geo']
            self.add_to_map(geo,tokens)
            
            