import requests
import sys
import simplejson

for line in sys.stdin:
    r = requests.get("https://api.twitter.com/1/users/show.json?screen_name=%s" % line.strip())
    for l in r.iter_lines():
	j = simplejson.loads(l)
	print j["id"]
