#!/usr/bin/env python
# encoding: utf-8
"""
s3writer.py

Created by Maksim Tsvetovat on 2011-12-22.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import sys
import os
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import datetime

class s3writer(object):
    """stores json files in an S3 bucket for the website to pick up"""
    
    def __init__(self):
        aws_access_key='AKIAIC65JLYAEJA7IRBA'
        aws_secret_key='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'
        self.base_url='data.electiongauge.com'
        self.conn = S3Connection(aws_access_key, aws_secret_key)
        self.public_bucket= self.conn.create_bucket('egauge')
        self.private_bucket= self.conn.create_bucket('egauge_private')
        self.dir={}
        
    def write(self,name,content,private=False):
        """Store *content* in a location designated by *key* in a public bucket (default) or private bucket (if private=True)"""
        if private:
            bucket=self.private_bucket
        else:
            bucket=self.public_bucket
        
        k = Key(bucket)
        k.key=name
        #k.set_metadata('content-type', 'text/plain')
        k.set_contents_from_string(content)
        if not private:
            self.dir[name]=str(datetime.datetime.now())
        
    def read(self,key,private=False):
        """get content from a location designated by *key* in a public bucket (default) or private bucket (if private=True)"""
        if private:
            bucket=self.private_bucket
        else:
            bucket=self.public_bucket

        k = Key(bucket)
        k.key=key
        return(k.get_contents_as_string())
        
    def update_public_index(self):
        html_head="<html><body>\n"
        html_foot="</body></html>\n"
        
        html=html_head
        for k,v in self.dir.iteritems():
            html+='<a href=\"'+k+'\">'+k+"</a>:"+v+"\n"
        
        html+=html_foot
        self.write("index.html",html)