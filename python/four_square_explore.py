import os
import json
from datetime import datetime
import foursquare

client_id = 'W5UZGTZGO2TJELFWQF1IPYWJ2UXX1WEY2FFZBS14QLXOBKS1'#os.environ['FOURSQUARE_ID']
client_secret = 'C2RXMQINBN3ZAOBX3QIOBTYVGXDGWYTPRO5GKNWL0AOC4T12'#os.environ['FOURSQUARE_SECRET']
redirect = 'http://sg20141.sb02.stations.graphenedb.com:24789/browser/'#os.environ['FOURSQUARE_REDIRECT']

query = 'topPicks'
#queries = ['food', 'drinks', 'coffee', 'shops', 'arts', 'outdoors', 'sights', 'specials', 'topPicks']
queries = ['arts', 'sights', 'specials', 'topPicks']


# Construct the client object
client = foursquare.Foursquare(client_id=client_id, client_secret=client_secret, redirect_uri=redirect)

def drange(start, stop, step):
    r = start
    while r < stop:
        yield r
        r += step

def get_checkins(ll, query):
    # Assign a search radius
    rad = '150'
    # get the response from the API
    response = client.venues.explore(params={'ll': ll, 'radius': rad, 'section': query, 'limit': '1000000'})
    return response

def get_venue(check_id):
    # Get client response
    r = client.venues(check_id)
    print r
    # Construct an empty dictionary for the properties
    properties = {}
    # Get the information of the venue
    venue = r['venue']
    # Add keys to the dictionary
    properties['place_id'] = check_id
    properties['name'] = venue['name']
    properties['user'] = [item['user']['id'] for item in venue['tips']['groups'][0]['items']]
    properties['checkins'] = venue['stats']['checkinsCount']
    properties['users_count'] = venue['stats']['usersCount']
    properties['category'] = venue['categories'][0]['name']
    properties['latitude'] = venue['location']['lat']
    properties['longitude'] = venue['location']['lng']
    try: properties['rating'] = venue['rating']
    except: properties['rating'] =  ''
    try: properties['hours'] = venue['hours']['timeframes']
    except: properties['hours'] = ''
    try: properties['twitter'] = venue['contact']['twitter']
    except: properties['twitter'] = ''
    try: properties['popular'] = venue['popular']['timeframes']
    except: properties['popular'] = ''
    properties['time'] = str(datetime.now())
    properties['data_source'] = 'foursquare_explore'
    
    # return the dictionary of properties
    return properties

sw = '22.1538, 113.8352'
ne = '22.5622, 114.4416'

if __name__=='__main__':
    # Construct a dictionary for all the checkins
    

    # since the api only returns up to 50 places at the time,
    # we construct a series of locations, and loop through them to scrape it
    sn_range = list(drange(22.1538, 22.5622, .003)) # 50.5 mts radius
    we_range = list(drange(113.8352, 114.3416, .003)) # 50.5 mts radius # 113.8352
    print len(sn_range), len(we_range)
    # for every latitude
    for n in sn_range[134:]:
        # for every longitude
        for e in we_range[30:150]:
            # construct a location
            ll = str(n) + ', ' + str(e)
            print ll
            
            try:
                # Get all the checkins for a given location
                t = get_checkins(ll, query)
                new_checkins = t['groups'][0]['items']
                all_checkins = {}
                # for every checkin in the checkinsggggg
                for checkin in new_checkins:
                    # Get the venue ID
                    check_id = checkin['venue']['id']
                    # if the id is not in the dictionary, add it
                    if check_id not in all_checkins:
                        all_checkins[check_id] = get_venue(check_id)
                #print len(all_checkins)
                # write the json to a file
                if len(all_checkins) > 0:
                    with open( '/Volumes/XP/Documents and Settings/Carlos Emilio/My Documents/sg2014/4sq/topPicks/%s,%sfour_explore.json' %(str(sn_range.index(n)), str(we_range.index(e))), 'w' ) as f:
                        f.write(json.dumps(all_checkins))
                    print 333333838383838383838383838383838383838383838383838
            except: pass

