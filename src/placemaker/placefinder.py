#!/usr/bin/env python
# encoding: utf-8
# Written by Brandon Diamond 
# Released into the public domain 
import urllib 

from django.utils import simplejson as json 

class YahooException(Exception): 
  pass 
  
# interface that behaves similarly to geopy's geocoders 
class placefinder(object): 
    
    def __init__(self, api_key):
        self.api_key = api_key
    
    @classmethod 
    def strip_result(cls, result): 
        if not result['postal']: 
          result['postal'] = result.get('uzip', '') 
        place = '%(city)s, %(statecode)s %(postal)s' % result 
        # return things in a geopy compatible format 
        return place, (float(result['latitude']), float(result['longitude'])) 
    
    def geocode(self, query, exactly_one=False): 
        try: 
          results = [YahooGeocode.strip_result(r) for r in placefind(query)] 
          return results[0] if exactly_one else results 
        except YahooException: 
          return None 
      
    def placefind(self, query): 
      file = urllib.urlopen("http://where.yahooapis.com/geocode?%s" % 
        urllib.urlencode({ 
            'appid': self.api_key, 
            'flags': 'j', 
            'q': query 
          })) 
      try: 
        result = json.loads(file.read()) 
        return result['ResultSet']['Results'] 
      except: 
        raise YahooException() 
      finally: 
        file.close()
        
        
