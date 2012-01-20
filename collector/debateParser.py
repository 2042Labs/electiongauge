#!/usr/bin/env python
# encoding: utf-8
"""
debateParser.py

Parses transcripts of political debates and sorts them by who-said-what.

Created by Maksim Tsvetovat on 2012-01-10.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import candidates as c
import requests
import BeautifulSoup as soup
import logging
import settings

l=logging.getLogger('DebateParser')

url="http://blogs.suntimes.com/sweet/2012/01/south_carolina_gop_cnn_debate_.html"

speaker_map={
'KING': 'king',
'PAUL': 'ronpaul',
'PERRY': 'perry',
'GINGRICH': 'gingrich',
'ROMNEY': 'romney',
'SANTORUM': 'santorum',
'HUNTSMAN': 'huntsman'
}

done=False
current_speaker=""
speaker_content={}



"""
#get the debate text 
html=requests.get(url).content
sp=soup.BeautifulSoup(html)
content=sp.findAll(id='entrytext')
paras=str(content[0]).replace('<p>','').replace('\n','').split('</p>')
"""



f=open(settings.corpusPath+'CSDebate.txt')
paras=[p for p in f]


for key in speaker_map.keys():
    speaker_content[key]=""

for p in paras:
    ##skip things that start with a tag
    if p.startswith('<') or p.startswith('('): continue
    
    ## if a paragraph starts witha speaker name, the content goes to the speaker
    for key in speaker_map.keys():
        if p.startswith(key):
            current_speaker=key
            speaker_content[key]+=p.replace(key,'')
            done=True
    
    ## if a paragraph has not been absorbed yet, give it to the last speaker
    if not done:    
        if current_speaker != '':
            speaker_content[current_speaker]+=p.replace(current_speaker,'')
            
    done=False

for key in speaker_map.keys(): 
    if speaker_map[key] in c.candidates:
        l.info("updating cropus for"+key)
        open(settings.corpusPath+speaker_map[key]+'.txt','a').write(speaker_content[key]+"\n")
