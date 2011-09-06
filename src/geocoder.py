import placemaker as pm_module
import placemaker.placefinder as pf_module
import placemaker.Yahoo as yy_module
import geopy
import logging

class geocoder(object):
    
    _yahoo_api_key='dj0yJmk9Qm9UQVljSEVMUlpRJmQ9WVdrOWNscEVPRGcwTldrbWNHbzlNVGMzTVRBeE56QTJNZy0tJnM9Y29uc3VtZXJzZWNyZXQmeD03MQ--'
    _yahoo_secret='eeae1d9c40a5a5eec7aea5505c90c0115b799e9f'

    def __init__(self):
        self._yy=yy_module.Yahoo(self._yahoo_api_key)
        self.cache={}
        
        logging.basicConfig()
        self.l = logging.getLogger('geocoder')
        self.l.setLevel(4) ## set debug level to "every fucking thing"

        #TODO: load saved dictionary

    def parse_point(self,str_pt):
        lat,lon=map(float, str_pt.split())
        # round to ~80 meters
        return [round(x, 3) for x in [lat, lon]]

    def geocode(self,loc,point):
        place=''
        
        try:
            if loc in self.cache: 
                place=self.cache[loc]
            elif point in self.cache: 
                place=self.cache[point]
            elif point is not '':         
                place=self._yy.reverse(self.parse_point(point))
                self.cache[point]=place   
            elif loc is not '':
                place=self._yy.geocode(loc)
                self.cache[loc]=place
        except Exception, ex:
            self.l.warning(type(ex))
            return '','','','','',''
              
        if place is not '':           
            return place
        else:
            return None
