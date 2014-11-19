from os import listdir
from os.path import isfile, join
from ttp import ttp
import json
import csv

twi_path = 'twitter/'
twi_jsons = [ f for f in listdir(twi_path) if isfile(join(twi_path,f)) ]
csv_file = open('csv/tweet_csv.csv', 'wt')

writer = csv.writer(csv_file)
writer.writerow(['lat', 'lon', 'time', 'content', 'tags'])

cnt = 0
for f in twi_jsons:
    with open('twitter/%s' %(f)) as json_file:
        tweets = json.load(json_file).values()
        for tweet in tweets:
            content = tweet['content']
            p = ttp.Parser()
            parsed_tweet = p.parse(content)
            hashtags = [tag.encode('utf-8') for tag in parsed_tweet.tags]
            if float(tweet['lat']) != 0 and float(tweet['lon']) != 0:
                writer.writerow([tweet['lat'], tweet['lon'], tweet['time'], tweet['content'].encode('utf-8'), str(hashtags)])
                cnt += 1
            

print cnt

csv_file.close()

