#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 18:20:15 2020

@author: qyang
"""

import twitter
import yaml

with open('~/~/data/config.yaml') as file:
    documents = yaml.full_load(file)

    for item, doc in documents.items():
        print(item, ":", doc)

consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''
api = twitter.Api(consumer_key=[consumer_key]
                  ,consumer_secret=[consumer_secret]
                  ,access_token_key=[access_token]
                  ,access_token_secret=[access_token_secret])

results = api.GetSearch(raw_query="q=twitter%20&result_type=recent&since=2014-07-19&count=12")

#%% 
#Import the Twython class
from twython import Twython
import pandas as pd

# Instantiate an object
python_tweets = Twython(consumer_key, consumer_secret)

# Create our query
query = {'q': 'learn python',
        'result_type': 'popular',
        'count': 10,
        'lang': 'en',
        }

# Search tweets
dict_ = {'user': [], 'date': [], 'text': [], 'favorite_count': []}
for status in python_tweets.search(**query)['statuses']:
    dict_['user'].append(status['user']['screen_name'])
    dict_['date'].append(status['created_at'])
    dict_['text'].append(status['text'])
    dict_['favorite_count'].append(status['favorite_count'])

# Structure data in a pandas DataFrame for easier manipulation
df = pd.DataFrame(dict_)
df.sort_values(by='favorite_count', inplace=True, ascending=False)
df.head(5)

#%%
from twython import TwythonStreamer
import csv

# Filter out unwanted data
def process_tweet(tweet):
    d = {}
    d['hashtags'] = [hashtag['text'] for hashtag in tweet['entities']['hashtags']]
    d['text'] = tweet['text']
    d['user'] = tweet['user']['screen_name']
    d['user_loc'] = tweet['user']['location']
    return d
    
    
# Create a class that inherits TwythonStreamer
class MyStreamer(TwythonStreamer):     

    # Received data
    def on_success(self, data):

        # Only collect tweets in English
        if data['lang'] == 'en':
            tweet_data = process_tweet(data)
            self.save_to_csv(tweet_data)

    # Problem with the API
    def on_error(self, status_code, data):
        print(status_code, data)
        self.disconnect()
        
    # Save each tweet to csv file
    def save_to_csv(self, tweet):
        with open(r'saved_tweets.csv', 'a') as file:
            writer = csv.writer(file)
            writer.writerow(list(tweet.values()))
            
# Instantiate from our streaming class
stream = MyStreamer(consumer_key, consumer_secret, access_token, access_token_secret)
# Start the stream
stream.statuses.filter(track='python')