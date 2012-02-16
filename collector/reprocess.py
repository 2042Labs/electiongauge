#!/usr/bin/env python
# encoding: utf-8
"""
reprocess.py

Created by Maksim Tsvetovat on 2012-02-15.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import simplejson as json 
from mapmaker import mapmaker
from timeline_maker import timeline_maker
from dateutil import parser

mm=mapmaker(interval=1000, to_file=True, to_s3=False)
tm=timeline_maker(interval=1000, to_file=True, to_s3=False)
#dm = discourse_mapper(interval=1000)

filez=os.listdir('../tmp')
for file in filez:
#file=filez[0]
    f_in=open('../tmp/'+file,'rb')
    timestamp=parser.parse(file.split('d')[1])
    print "<<<<"+file+">>>>>"
    for line in f_in:
        try:
            js=json.loads(line)
        except:
            continue
    
        tokens=js['tokens']
        place=js['geo']
    
        mm.add_to_map(place,tokens)
        ##Add tweet to the timeline
        tm.add_to_timeline(tokens,timestamp=timestamp)
    
        print '.',
    print "@@@@@"