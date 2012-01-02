#!/usr/bin/env python
# encoding: utf-8
"""
discourse_mapper.py

Created by Maksim Tsvetovat on 2011-12-20.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import simplejson as json
from collections import defaultdict
import logging as l

import cunning_linguist as cl
import candidates as can
import states as st
import s3writer

from wordbag import wordbag
import networkx as net

class discourse_mapper(object):

    def __init__(self,interval=100):
        self.s3=s3writer.s3writer()
        self.wb=wordbag()
        self.interval=interval
        self.counter=0
        
        ## try to load previous state of the discourse mapper. 
        ## On failure, rebuild corpus
        try:
            wb.load()
        except:        
            self._load_corpus()


    def _load_corpus(self):
        for key in can.candidates.keys():
            try:
                text=open('../egauge/data/corpus/'+key+'.txt','rb').read()
            except: 
                continue
        
            tokens=cl.process(text)
            self.wb.add_tokens(key,tokens)
    
        self.wb.prune()
    
    def add(self,place,tokens):
        self.counter+=1
        #print place['country']
        if place['country'] == 'United States':
            state=place['statecode']
            #print state, tokens
            self.wb.add_tokens(state,tokens)
            
        if self.counter>=self.interval:
            self._write_data(self.compute_metrics())


    def compute_metrics(self):
        gauges=defaultdict(dict)

        ## for every state, every candidate, compute a linguistic match
        for state in st.states:
            try:
                ss= set(self.wb.word_graph[state].keys())
            except KeyError:
                continue ## we have no data for this state, we skip it
                
            for key in can.candidates.keys():
                cs= set(self.wb.word_graph[key].keys())
                ## Compute intersection between state discourse and candidate
                p=cs & ss
                gauges[state][key]=float(len(p))/float(len(ss)+len(cs))
        
        return gauges

    def _write_data(self, gauges, to_s3=True, to_file=True):
        """Write out map data as JSON files to S3, to a local file OR BOTH"""
        l.debug(">>>>Writing out discourse gauges")
        
        if to_file:
            f="../egauge/data/json/gauge.json"
            out=open(f,'wb')
            out.write(json.dumps(gauges))
        if to_s3:
            f="gauges.json"
            self.s3.write(f, json.dumps(gauges))

    def test(self):
        infile=open('/tmp/test_output.json')
        for line in infile:
            
            try :
                js=json.loads(line)
            except:
                l.info(line)
                l.info("discourse mapper parse error")
                continue
                
            tokens=js['tokens']
            geo=js['geo']
            self.add(geo,tokens)


        