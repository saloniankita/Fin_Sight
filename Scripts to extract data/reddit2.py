# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 00:36:02 2020

@author: bhanvi
"""


import praw

import json
import time
import math
import requests
import itertools
import numpy as np


from datetime import datetime, timedelta

def give_me_intervals(start_at, number_of_days_per_interval = 3):
    
    end_at = math.ceil(datetime.utcnow().timestamp())
        
    ## 1 day = 86400,
    period = (86400 * number_of_days_per_interval)

    end = start_at + period
    yield (int(start_at), int(end))

    padding = 1
    while end <= end_at:
        start_at = end + padding
        end = (start_at - padding) + period
        yield int(start_at), int(end)

def make_request(uri, max_retries = 5):
    def fire_away(uri):
        response = requests.get(uri)
        assert response.status_code == 200
        return json.loads(response.content)

    current_tries = 1
    while current_tries < max_retries:
        try:
            response = fire_away(uri)
            return response
        except:
            time.sleep(.150)
            current_tries += 1

    return fire_away(uri)
 
def pull_posts_for(subreddit, start_at, end_at):
    
    def map_posts(posts):
        return list(map(lambda post: {
            'id': post['id'],
            'created_utc': post['created_utc'],
            'prefix': 't4_'
        }, posts))
    
    SIZE = 500
    URI_TEMPLATE = r'https://api.pushshift.io/reddit/search/submission?subreddit={}&after={}&before={}&size={}'
    
    post_collections = map_posts( \
        make_request( \
            URI_TEMPLATE.format(subreddit, start_at, end_at, SIZE))['data'])

    n = len(post_collections)
    while n == SIZE:
        last = post_collections[-1]
        new_start_at = last['created_utc'] - 10
        
        more_posts = map_posts( \
            make_request( \
                URI_TEMPLATE.format(subreddit, new_start_at, end_at, SIZE))['data'])
        
        n = len(more_posts)
        post_collections.extend(more_posts)

    return post_collections


subreddit = 'Artificial Intelligence'

end_at = math.ceil(datetime.utcnow().timestamp())
start_at = math.floor((datetime.utcnow() - timedelta(days=10)).timestamp())

posts = pull_posts_for(subreddit, start_at, end_at)

print('found:', len(posts))
print('unique:', len(np.unique([ post['id'] for post in posts ])))



## assert no dups,
sorted_by_occurence = sorted([ (k, len(list(g))) for k,g in itertools.groupby(posts, lambda x: x['id']) ], key=lambda x: x[1], reverse=True)
print(sorted_by_occurence[:10])


## quick look at the posts,
print(posts[:10])



start_at = math.floor(\
    (datetime.utcnow() - timedelta(days=20)).timestamp())

posts = []
for interval in give_me_intervals(start_at, 7):
    pulled_posts = pull_posts_for(
        subreddit, interval[0], interval[1])
    
    posts.extend(pulled_posts)


posts_from_reddit = []
comments_from_reddit = []

reddit = praw.Reddit(client_id= 'O2VsVgcMY3JaUw', 
                     client_secret= 'LZ14ajDsvPAyS7QXbf6aa9RstTGxrQ', 
                     refresh_token= '585373841541-3eM4UGc3KGz_XlcmjJWjmB1LE__06Q',
                     user_agent='test app1')

TIMEOUT_AFTER_COMMENT_IN_SECS = .250

for submission_id in np.unique([ post['id'] for post in posts ]):
    submission = reddit.submission(id=submission_id)

    posts_from_reddit.append(submission)

    submission.comments.replace_more(limit=None)
    for comment in submission.comments.list():
        comments_from_reddit.append(comment)
        
        if TIMEOUT_AFTER_COMMENT_IN_SECS > 0:
            time.sleep(TIMEOUT_AFTER_COMMENT_IN_SECS)
            

print(len(comments_from_reddit))
print(len(posts_from_reddit))