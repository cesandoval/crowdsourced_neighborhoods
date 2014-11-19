import os
import json
import time
import sys
from datetime import datetime
import foursquare

sys.path.insert(0, '../')
#from s3 import upload_to_s3

# Set the API keys
client_id = 'W5UZGTZGO2TJELFWQF1IPYWJ2UXX1WEY2FFZBS14QLXOBKS1'
client_secret = 'C2RXMQINBN3ZAOBX3QIOBTYVGXDGWYTPRO5GKNWL0AOC4T12'
redirect = 'http://sg20141.sb02.stations.graphenedb.com:24789/browser/'

# Set some query parameters
#ll = '40.7127, -74.0059' #NY
total_time = 150 

def get_checkins(ll):
    # Construct the client object
    client = foursquare.Foursquare(client_id=client_id, client_secret=client_secret, redirect_uri=redirect)
    # get the response from the API
    response = client.venues.trending(params={'near': ll, 'limit':'1000', 'radius': '7500'})
    return response

def get_many_checkins(lls, total_time, names):
    all_checkins = {}
    remaining_seconds = total_time
    interval = 15

    while remaining_seconds > 0:
        added = 0
        for nid, ll in enumerate(lls):
            print 'scrapping: ', names[nid]
            t = get_checkins(ll)
            #print t
            new_checkins = t['venues']
            for checkin in new_checkins:
                check_id = checkin['id']
                if check_id not in all_checkins:
                    properties = {}
                    
                    properties['content'] = checkin['name']
                    properties['here_now'] = checkin['hereNow']['count']
                    properties['checkins'] = checkin['stats']['checkinsCount']
                    properties['category'] = checkin['categories'][0]['name']
                    properties['lat'] = checkin['location']['lat']
                    properties['lon'] = checkin['location']['lng']
                    properties['checkins'] = checkin['stats']['checkinsCount']
                    properties['users_count'] = checkin['stats']['usersCount']
                    properties['place_id'] = check_id
                    properties['data_point'] = 'none'
                    properties['raw_source'] = checkin
                    properties['time'] = str(datetime.now())
                    properties['data_source'] = 'foursquare_trending'
                    
                    all_checkins[check_id] = properties
                    added += 1
        print "At %d seconds, added %d new checkins, for a total of %d" % ( total_time - remaining_seconds, added, len(all_checkins))
        time.sleep(interval)
        remaining_seconds -= interval
    return all_checkins
    
def run(lls, names):
    checkins = get_many_checkins(lls, total_time, names)
    #target_path = 'foursquare/%sfoursquare_trending.json' %(str(datetime.now()))
    name =  str(datetime.now()).replace(" ", "_")
    name = name.replace('.', '_')
    name = name.replace(':', '_')
    
    #upload = upload_to_s3( target_path, json.dumps(checkins))
    with open( 'foursquare/%sfour_trending.json' %(name), 'w' ) as f:
        f.write(json.dumps(checkins))


lls = ['40.7127, -74.0059', '40.634525, -73.945806', '40.608628, -74.086612', '40.703947, -73.84949', '40.830848, -73.916423']
names = ['NY', 'Brooklyn', 'Staten Island', 'Queens', 'Bronx']

all_time = 9000000000000000000
while all_time > 0:
    run(lls, names)
    all_time -= 30
