#!/usr/bin/env python
# encoding: utf-8
"""
discourse_mapper.py

Created by Maksim Tsvetovat on 2011-12-20.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import sys
import os

import cunning_linguist as cl
import candidates as can
from wordbag import wordbag

wb=wordbag()

def load_corpus():
    for key in can.candidates.keys():
        try:
            text=open('../egauge/data/corpus/'+key+'.txt','rb').read()
        except: 
            continue
        
        tokens=cl.process(text)
        wb.add_tokens(key,tokens)
        
        