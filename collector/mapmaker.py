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
   # self.count=0
#    self.zip_can={}
    
    def __init__(self, interval=10): 
        self.count=0
        self.interval=interval
        self.zip_can={}
        for key in can.candidates.keys():
            self.zip_can[key]={}
        self.db=self._read_ziptable()
            
    ### read the csv file 
    def _read_ziptable(self):
        db={}
        for row in csv.reader(open('zip2county.csv','rU')):
            db[row[0]]=row[1]
        return db
        
            
    def intersect(self, a, b):
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
                    
                print zzip, county
                
                if self.intersect(tokens,can.candidates[key]) != []:
                    if county in self.zip_can[key]:
                        self.zip_can[key][county]+=1
                    else:
                        self.zip_can[key][county]=1
                    
        ##if it's been a while since the last write, do a write now, and resent counter
        if self.count >= self.interval:
            self.dump()
            self.count=0            
                    
    def dump(self):
        l.info(">>>>Writing out choropleths")
        f="/tmp/zipmap_"
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
            
