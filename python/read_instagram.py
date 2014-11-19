from os import listdir
from os.path import isfile, join
from ttp import ttp
import json
import csv

insta_path = 'instagram/'
insta_jsons = [ f for f in listdir(insta_path) if isfile(join(insta_path,f)) ]
csv_file = open('csv/instagram_csv.csv', 'wt')

writer = csv.writer(csv_file)
writer.writerow(['lat', 'lon', 'time', 'content', 'tags'])

cnt = 0
all_ids = []
for f in [insta_jsons[0]]:
    with open('instagram/%s' %(f)) as json_file:
        grams = json.load(json_file)
        
        # every instagram json has a number of lists with a dictionary that has a data attribute which is a list of pics on its own
        #print json.dumps(grams[3]['data'][0])
        #print len(grams)
        
        for gram in grams:
            if gram != None:
                if len(gram['data']) != 0:
                    print gram['data']
                    # check if the id of the gram is in all_ids....
            #content = gram['content']
            
            '''
            p = ttp.Parser()
            parsed_gram = p.parse(content)
            hashtags = [tag.encode('utf-8') for tag in parsed_gram.tags]
            if float(gram['lat']) != 0 and float(gram['lon']) != 0:
                writer.writerow([gram['lat'], gram['lon'], gram['time'], gram['content'].encode('utf-8'), str(hashtags)])
                cnt += 1'''
            

print cnt

csv_file.close()

'''
type of data we have..... gis, social media

what are we trying to get from tweets?
what characterizes a neighborhood?
4sq
-venue types

twitter
-how twitter is used:
    -times
    -density
    -length of tweets
    - how to find activities that are unique to a particular location?
'''