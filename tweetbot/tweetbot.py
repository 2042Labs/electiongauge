#!/usr/bin/env python
# encoding: utf-8
"""
tweetbot.py

Created by Maksim Tsvetovat on 2012-01-16.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

import tweepy

username = "ElectionGauge"
password = "cssgmu"

CONSUMER_KEY = 'zSxtDpHrZ8GpSimb1k4DA'
CONSUMER_SECRET = 't1D97sSvjumR6iWLjvl1q95V0gs7ieWVyLJpzQAnBUw'
ACCESS_KEY = '365574554-eNVd7Xp8jYooqhXBEsd5xi7kCZqA6X7ZMNferWbV'
ACCESS_SECRET = 'nTIAxmLjaKa6oFHBj5ZbqBvofzuiM4YGYir7fyA5hc'


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
#auth = tweepy.BasicAuthHandler(username, password)
api = tweepy.API(auth)

api.update_status("test...1..2..3")