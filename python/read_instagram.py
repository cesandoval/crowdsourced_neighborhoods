from os import listdir
from os.path import isfile, join
from ttp import ttp
import json
import csv

insta_path = 'instagram/'
insta_jsons = [ f for f in listdir(insta_path) if isfile(join(insta_path,f)) ]
csv_file = open('csv/instagram_csv.csv', 'wt')

writer = csv.writer(csv_file)
writer.writerow(['pid', 'lat', 'lon', 'time', 'content', 'tags'])


all_ids = []
for f in insta_jsons:
    with open('instagram/%s' %(f)) as json_file:
        grams = json.load(json_file)
        cnt = 0
        for gram in grams:
            if gram != None:
                if len(gram['data']) != 0:
                    for data in gram['data']:
                        #image, user, content, time, iid, lat, lon = '', '', '', '', '', '', ''
                        content, image, user, caption, time, iid, lat, lon = '', None, None, None, None, None, None, None
                        try: image = data['images']['standard_resolution']['url']
                        except: pass
                        try: user = data['user']['id']
                        except: pass
                        try: content = data['caption']['text']
                        except: pass
                        try: time = data['caption']['created_time']
                        except: pass
                        try: iid = data['id']
                        except: pass
                        try: lat = data['location']['latitude']
                        except: pass
                        try: lon = data['location']['longitude']
                        except: pass
                        raw_source = data
                        
                        if lat != None and lon != None:
                            if iid not in all_ids:
                                p = ttp.Parser()
                                hashtags = None
                                parsed_gram = p.parse(content)
                                hashtags = [tag.encode('utf-8') for tag in parsed_gram.tags]
                                #print hashtags
                                writer.writerow([iid, lat, lon, time, content.encode('utf-8'), str(hashtags)])
                                
                                all_ids.append(iid)
                                cnt += 1                        
                        
    print "Added %d new grams, for a total of %d" % (cnt, len(all_ids))                        

csv_file.close()
