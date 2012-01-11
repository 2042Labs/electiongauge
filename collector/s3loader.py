#!/usr/bin/env python
# encoding: utf-8
"""
s3loader.py

Created by Maksim Tsvetovat on 2012-01-11.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

import s3writer
from candidates import candidates
import settings
import logging as l


s3=s3writer.s3writer()

manifest=["zipmap_"+key+".json" for key in candidates.keys()]
manifest.extend(["timeline_"+key+".json" for key in candidates.keys()])
manifest.extend(['gauges.js'])

for key in manifest:
    filename=settings.jsonPath+key
    l.debug("fetching "+key+" to "+filename)
    f=open(filename,'wb')
    f.write(s3.read(key))

l.info("Updated local gauges")