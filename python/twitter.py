import os
import json
import time
import sys

from datetime import datetime
from twython import Twython

#sys.path.insert(0, '../')
#from s3 import upload_to_s3

APP_KEY = '5g8MCsu7a2e74JRORQ22G76uy'
APP_SECRET = 'qcwgzUGzgELMFRHQI1tZqsZtvkTTbQxp7KUnjQnR3WjKMin0Ff'

def get_tweets( latlong=None ):
    ''' Fetches tweets with a given query at a given lat-long.'''
    twitter = Twython( APP_KEY, APP_SECRET )
    results = twitter.search( geocode=','.join([ str(x) for x in latlong ]) + ',15km', result_type='recent', count=100 )
    return results['statuses']


def get_lots_of_tweets( latlongs, names):
    """ Does pretty much what its long name suggests. """
    all_tweets = {}
    total_time = 150
    remaining_seconds = total_time
    interval = 15 
    while remaining_seconds > 0:
        added = 0
        new_tweets = []
        for nid, latlong in enumerate(latlongs):
            print 'scrapping: ', names[nid]
            new_tweets.extend(get_tweets( latlong ))
        for tweet in new_tweets:
            tid = tweet['id']
            if tid not in all_tweets and tweet['coordinates'] != None:
                properties = {}
                properties['lat'] = tweet['coordinates']['coordinates'][0]
                properties['lon'] = tweet['coordinates']['coordinates'][1]
                properties['tweet_id'] = tid
                properties['content'] = tweet['text']
                properties['user'] = tweet['user']['id']
                properties['user_location'] = tweet['user']['location']
                properties['raw_source'] = tweet
                properties['data_point'] = 'none'
                properties['time'] = tweet['created_at']
                all_tweets[ tid ] = properties
                added += 1
        print "At %d seconds, added %d new tweets, for a total of %d" % (total_time - remaining_seconds, added, len( all_tweets ) )
        time.sleep(interval)
        remaining_seconds -= interval
    return all_tweets


def run(locations, names):
    #for nid, location in enumerate(locations):
    t = get_lots_of_tweets(locations, names)
    name =  str(datetime.now()).replace(" ", "_")
    name = name.replace('.', '_')
    name = name.replace(':', '_')
    # = 'twitter/%stweets.json' %(str(datetime.now()))
    with open('twitter/%stweets.json' %(name), 'w' ) as f:
        f.write( json.dumps(t))
    #upload = upload_to_s3( target_path, json.dumps(t))

locations = [[40.7127, -74.0059], [40.634525, -73.945806], [40.608628, -74.086612], [40.703947, -73.84949], [40.830848, -73.916423]]
names = ['NY', 'Brooklyn', 'Staten Island', 'Queens', 'Bronx']
all_time = 9000000000000000000
while all_time > 0:
    run(locations, names)
    all_time -= 30

'''    
Brooklyn:
[40.634525, -73.945806]

Staten Island:
[40.608628, -74.086612]

Queens:
[40.703947, -73.84949]

Bronx:
[40.830.848, -73.916423]'''