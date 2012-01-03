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
import logging
l=logging.getLogger("TWEET_SAVER")

class tweet_saver(object):
    
    def __init__(self,name="tweet",private=False,limit=1000):
        self.name=name
        self.s3=s3writer.s3writer()
        self.toWrite = ""
        self.counter = 0
        self.limit = limit
        self.private=private
        l.info("Initialized <<tweet_saver>>, limit %d", self.limit)

    def add(self,js):
        l.debug("add: "+str(self.counter))
        self.counter += 1    
        self.toWrite+=js+"\n"
        
        if self.counter>=self.limit:
            self._dump()
            self.toWrite=""
            self.counter=0
    
    def _dump(self):
        l.info("saving buffer")
        time=str(datetime.datetime.now())
        self.s3.write(self.name+time,self.toWrite,private=self.private)