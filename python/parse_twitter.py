from os import listdir
from os.path import isfile, join
from ttp import ttp
from nltk.corpus import stopwords

import json
import csv

def parse_jsons(twi_path):
    twi_jsons = [ f for f in listdir(twi_path) if isfile(join(twi_path,f)) ]
    
    all_ids = []
    for f in twi_jsons:
        with open('%s%s' %(twi_path, f)) as json_file:
            tweets = json.load(json_file).values()
            for tweet in tweets:
                content = tweet['content']
                p = ttp.Parser()
                #parsed_tweet = p.parse(content)
                #hashtags = [tag.encode('utf-8') for tag in parsed_tweet.tags]
                if float(tweet['lat']) != 0 and float(tweet['lon']) != 0:
                    if tweet['tweet_id'] not in all_ids:
                        all_ids.append(tweet['tweet_id'])
                        yield tweet['content'].encode('utf-8')
    
def make_texts(tweets):
    stoplist = stopwords.words('english')
    for tweet in tweets:
        yield [word for word in tweet.lower().split() if word not in stoplist]
    

twi_path = 'twitter/'
tweets = parse_jsons(twi_path)
texts = make_texts(tweets)

all_tokens = sum(texts, [])
tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)

