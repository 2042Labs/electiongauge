#!/usr/bin/env python
# encoding: utf-8
"""
tweet_saver.py

Created by Maksim Tsvetovat on 2012-01-02.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import simplejson as json
import s3writer
import datetime
import logging as l

class tweet_saver(object):
    
    def __init__(self,name="tweet",private=False,limit=1000):
        self.name=name
        self.s3=s3writer.s3writer()
        self.toWrite = ""
        self.counter = 0
        self.limit = limit
        self.private=private
        l.log(l.INFO, "Initialized <<tweet_saver>>")

    def add(self,js):
        self.counter += 1    
        self.toWrite+=js+"\n"
        
        if self.counter>=self.limit:
            self._dump()
            self.toWrite=""
            self.counter=0
    
    def _dump(self):
        l.log(l.DEBUG, "TWEET_SAVER > saving buffer")
        time=str(datetime.datetime.now())
        self.s3.write(self.name+time,self.toWrite,private=self.private)