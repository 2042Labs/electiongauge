#!/usr/bin/env python
# encoding: utf-8
"""
timeline_maker.py

Created by Maksim Tsvetovat on 2011-12-20.
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
import datetime
import s3writer
import settings

l=logging.getLogger("TIMELINE")

class timeline_maker(object):
    
    def __init__(self, interval=10, resolution='minute'):
        self.s3=s3writer.s3writer()
        self.resolution=resolution
        self.count=0
        self.interval=interval
        self.timelines={}
        self.word_timelines={}
        ## check for existing files -- maybe we crashed and need to recover?
        f=settings.jsonPath+"timeline_"
        l.info("Initializing timelines")
        for key in can.candidates.keys():
            try :
                out=open(f+key+".json",'rb')
                self.timelines[key]=json.loads(out.read())           
            except IOError:            
                self.timelines[key]={}
    
    
    def _make_time_key(self,now):
        """ take a date and return a string key that corresponds to hourly or minute resolution"""
        year=now.year
        month=now.month
        day=now.day
        hour=now.hour
        minute=now.minute
        if self.resolution == 'hour':
            key=str(datetime.datetime(year,month,day,hour))
        else:
            key=str(datetime.datetime(year,month,day,hour,minute))
        return key
    
    def _intersect(self, a, b):
        """intersect 2 lists and return the result"""
        return list(set(a) & set(b))
    
    def add_to_timeline(self,tokens):
        """Send some tokens in here and -- if they match to a particular candidate, they'll be added to the timeline"""
        self.count+=1
        time=self._make_time_key(datetime.datetime.today())
        for key in can.candidates.keys():
            if self._intersect(tokens,can.candidates[key]) != []:
                if time in self.timelines[key]:
                    self.timelines[key][time]+=1
                else:
                    self.timelines[key][time]=1
    
        ##if it's been a while since the last write, do a write now, and resent counter
        if self.count >= self.interval:
            self._write_data()
            self.count=0

    def _dump(self):
        """Write out map data as JSON files"""
        l.info(">>>>Writing out timelines")
        f=settings.jsonPath+"timeline_"
        for key in self.timelines.keys():
            out=open(f+key+".json",'wb')
            out.write(json.dumps(self.timelines[key]))
            

    def _write_data(self, to_s3=True, to_file=True):
        """Write out map data as JSON files to S3, to a local file OR BOTH"""
        l.info(">>>>Writing out timelines")
        if to_file:
            f=settings.jsonPath+"timeline_"
            for key in self.timelines.keys():
                out=open(f+key+".json",'wb')
                out.write(json.dumps(self.timelines[key]))
        if to_s3:
            f="timeline_"
            for key in self.timelines.keys():
                self.s3.write(f+key+".json", json.dumps(self.timelines[key]))

    def test(self):
        infile=open(settings.jsonPath+'test_output.json')
        for line in infile:
            js=json.loads(line)
            tokens=js['tokens']
            self.add_to_timeline(tokens)


"""   
    def _pivot(self):
        ##write out stacked timelines
        stacked=defaultdict(dict)
        for key1 in self.timelines.keys():
            for key2 in self.timelines[key1]:
                stacked[key2][key1]=self.timelines[key1][key2]
        return stacked
        
    def _dump_pivot(self, to_s3=True, to_file=True):
        
        data=self._pivot()
        f=settings.jsonPath+"timeline_stacked.csv"
        fields=['time'].extend(self.timelines.keys())
        w.writerows(data)
"""


