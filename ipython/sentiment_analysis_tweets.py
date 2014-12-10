from os import listdir
from os.path import isfile, join
from ttp import ttp
from itertools import chain

import json
import csv

from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

UPPERLETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
LETTERS_AND_SPACE = UPPERLETTERS + UPPERLETTERS.lower() + ' \t\n'

def loadDictionary():
    dictionaryFile = open('dictionary.txt')
    englishWords = {}
    for word in dictionaryFile.read().split('\n'):
        englishWords[word] = None
    dictionaryFile.close()
    return englishWords

ENGLISH_WORDS = loadDictionary()

def getEnglishCount(message):
    message = message.upper()
    message = removeNonLetters(message)
    possibleWords = message.split()

    if possibleWords == []:
        # no words at all, so return 0.0
        return 0.0, ''  

    matches = 0
    all_words = []
    for word in possibleWords:
        if word in ENGLISH_WORDS:
            matches += 1
            all_words.append(word + ' ')
    return float(matches) / len(possibleWords), ''.join(all_words).lower()


def removeNonLetters(message):
    lettersOnly = []
    for symbol in message:
        if symbol in LETTERS_AND_SPACE:
            lettersOnly.append(symbol)
    return ''.join(lettersOnly)


def isEnglish(message, wordPercentage=20, letterPercentage=85):
    # By default, 20% of the words must exist in the dictionary file, and
    # 85% of all the characters in the message must be letters or spaces
    # (not punctuation or numbers).
    cnt, sentence = getEnglishCount(message)
    words_match = cnt * 100 >= wordPercentage
    numLetters = len(removeNonLetters(message))
    messageLettersPercentage = float(numLetters) / len(message) * 100
    letters_match = messageLettersPercentage >= letterPercentage
    return words_match and letters_match, sentence
    
def jsons_to_tuple(twi_path):
    twi_jsons = [ f for f in listdir(twi_path) if isfile(join(twi_path,f)) ]

    all_ids = []
    for f in twi_jsons:
        with open('%s%s' %(twi_path, f)) as json_file:
            tweets = json.load(json_file).values()
            for tweet in tweets:
                content = tweet['content']
                
                is_english, new_content = isEnglish(content, 20, 65)
                if is_english:
                    if float(tweet['lat']) != 0 and float(tweet['lon']) != 0:
                        if tweet['tweet_id'] not in all_ids:
                            all_ids.append(tweet['tweet_id'])
                            yield tweet['tweet_id'], tweet['lat'], tweet['lon'], new_content
                            
twi_path = '../python/twitter/'
tweets = jsons_to_tuple(twi_path)

def get_sentiment(text):
    blob = TextBlob(text, analyzer=NaiveBayesAnalyzer())
    return blob.sentiment
    
#with open('csv/sentiment_tweets.csv', 'wb') as fp:
#writer = csv.writer(fp, delimiter=',')
#writer.writerow( ('lat', 'lon', 'tweet', 'sentiment', 'pos', 'neg') )

for tweet in tweets:
    try:
        tid, lat, lon, content = tweet
        sentiment, pos, neg = get_sentiment(content)
        #writer.writerow([lat, lon, content, sentiment, pos, neg])
        with open('json_twitter/%ssentiment_tweet.json' %(tid), 'w' ) as f:
            f.write( json.dumps({'lat':lat, 'lon':lon, 'tweet':content, 'sentiment':sentiment, 'pos':pos, 'neg':neg}))
    except: pass
