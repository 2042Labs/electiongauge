import requests
import simplejson as json
from datetime import datetime
from datetime import date
from datetime import timedelta
from dateutil import parser
from collections import Counter
import matplotlib.pyplot as plot

def get_timeline(url):
    resp=requests.get(url)
    tml=json.loads(resp.content)

    time={}
    for dt in tml.keys():
        date=parser.parse(dt)
        time[date]=tml[dt]
    return time
    
def interpolate_hourly(time):
    sorted_time=sorted(time,reverse=True)

    hourly=Counter()
    hr=dy=mo=yr=-1 ##initialize date parts to impossible value
    key=0
    for d in sorted_time:
        if d.hour!=hr:
            yr=d.year
            mo=d.month
            dy=d.day
            hr=d.hour
            key=datetime(yr,mo,dy,hr)
        hourly[key]+=time[d]

    sorted_hourly=sorted(hourly,reverse=True)
    sorted_hourly_values=[hourly[h] for h in sorted_hourly]
    return sorted_hourly, sorted_hourly_values
    
def interpolate_daily(time):
    sorted_time=sorted(time,reverse=True)

    daily=Counter()
    hr=dy=mo=yr=-1 ##initialize date parts to impossible value
    key=0
    for d in sorted_time:
        if d.day!=dy:
            yr=d.year
            mo=d.month
            dy=d.day
            hr=d.hour
            key=datetime(yr,mo,dy,0)
        daily[key]+=time[d]

    sorted_daily=sorted(daily,reverse=True)
    sorted_daily_values=[daily[h] for h in sorted_daily]
    return sorted_daily, sorted_daily_values

def last_week(time,value):
    cutoff=datetime.today()-timedelta(0,0,0,0,0,0,1)
    


romney=get_timeline('http://s3.amazonaws.com/egauge/timeline_romney.json')
santorum=get_timeline('http://s3.amazonaws.com/egauge/timeline_santorum.json')
gingrich=get_timeline('http://s3.amazonaws.com/egauge/timeline_gingrich.json')
paul=get_timeline('http://s3.amazonaws.com/egauge/timeline_ronpaul.json')

romney_dates,romney_values = interpolate_hourly(romney)
santorum_dates,santorum_values = interpolate_hourly(santorum)
gingirch_dates,gingrich_values = interpolate_hourly(gingrich)
paul_dates,paul_values = interpolate_hourly(paul)

plot.plot_date(romney_dates, romney_values, 'b-')
plot.plot_date(santorum_dates, santorum_values, 'r-')
plot.plot_date(gingirch_dates, gingrich_values, 'g-')
plot.plot_date(paul_dates, paul_values, 'k-')
plot.savefig("hourly_averages.png")



romney_dates,romney_values = interpolate_daily(romney)
santorum_dates,santorum_values = interpolate_daily(santorum)
gingirch_dates,gingrich_values = interpolate_daily(gingrich)
paul_dates,paul_values = interpolate_daily(paul)

plot.plot_date(santorum_dates, santorum_values, 'r-')
plot.plot_date(gingirch_dates, gingrich_values, 'g-')
plot.plot_date(paul_dates, paul_values, 'k*-')
plot.savefig("daily_averages.png")

