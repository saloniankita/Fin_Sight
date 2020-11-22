# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 16:35:21 2020

@author: bhanvi
"""

import tweepy
import time
import pandas as pd

consumer_key = 'oH6Liu9jMUAo17mdqi0ziskPk'
consumer_secret = 'chL6IBdbf852EAhYkVECjVaVOLHEaTkmgEESyDIkl3JQeIVCQS'
access_token = '1258661197898891264-A42VQ78orL7RWlunrpA9fnzQ6D5YT3'
access_token_secret = '8VqOzoUWAR0UA7WZNrpaCwDmkUGOl4bZ1dRHcvULTZPSw'



auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)



text_query = 'SBI payment experience'
count = 200
tweets = []

def text_query_to_csv(text_query,count):
    try:
        # Creation of query method using parameters
        tweets = tweepy.Cursor(api.search,q=text_query).items(count)

        # Pulling information from tweets iterable object
        tweets_list = [[tweet.created_at, tweet.id, tweet.text] for tweet in tweets]

        # Creation of dataframe from tweets list
        # Add or remove columns as you remove tweet information
        tweets_df = pd.DataFrame(tweets_list,columns=['Datetime', 'Tweet Id', 'Text'])

        # Converting dataframe to CSV 
        tweets_df.to_csv('{}-tweet.csv'.format(text_query), sep=',', index = False)
        
    except BaseException as e:
        print('failed on_status,',str(e))
        time.sleep(3)
        
text_query_to_csv(text_query, count)