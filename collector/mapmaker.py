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
import logging as l
import bsddb
import csv

class mapmaker(object):
    """MapMaker is a class that generates county-by-county maps from tweets"""
    
    def __init__(self, interval=10): 
        self.count=0
        self.interval=interval
        self.zip_can={}
        ## check for existing files -- maybe we crashed and need to recover?
        f="../egauge/data/json/zipmap_"
        for key in can.candidates.keys():
            try :
                out=open(f+key+".json",'rb')
                self.zip_can[key]=json.loads(out.read())           
            except IOError:            
                self.zip_can[key]={}
        
        ## Initialize the zip-to-county table from a CSV file. 
        self.db=self._read_ziptable()
        
            
    ### read the csv file 
    def _read_ziptable(self,filename='zip2county.csv'):
        """Read a translation table zipcode -> county code"""
        db={}
        for row in csv.reader(open(filename,'rU')):
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
            self._dump()
            self.count=0            
                    
    def _dump(self):
        """Write out map data as JSON files"""
        l.info(">>>>Writing out choropleths")
        f="../egauge/data/json/zipmap_"
        for key in self.zip_can.keys():
            out=open(f+key+".json",'wb')
            out.write(json.dumps(self.zip_can[key]))
            
            
    def test(self):
        infile=open('/tmp/test_output.json')
        for line in infile:
            js=json.loads(line)
            tokens=js['tokens']
            geo=js['geo']
            self.add_to_map(geo,tokens)
            
