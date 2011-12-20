#!/usr/bin/env python
# encoding: utf-8
"""
sas_reader.py

Created by Maksim Tsvetovat on 2011-12-19.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import string
import csv
import bsddb

sasfile="zip2county.txt"
outfile="zip2county.csv"
#db = bsddb.btopen('zip_county.db', 'c')

out=csv.writer(open(outfile,'wb'))

for line in open(sasfile,'rb'):
    row=line.strip().split('\'')
#    print row
    if len(row)==5:
        county=row[3].strip().split(' ')
        fips=county[0]
        name='_'.join(county[1:])
        out.writerow([row[1],fips,name])
#        db[row[1]]=','.join([fips,name])
#        print "short:", row[1],">>",fips,">>",name
    elif len(row)==7:
        f=row[1]
        t=row[3]
        county=row[5].strip().split(' ')
        fips=county[0]
        name='_'.join(county[1:])

        for zz in range(int(f),int(t)+1):
            s_zip='%05d'%zz
            out.writerow([s_zip,fips,name])
 #           db[s_zip]=','.join([fips,name])
            #print "long:", s_zip,">>",fips,">>",name

db.sync()