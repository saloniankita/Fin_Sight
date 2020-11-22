# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 13:37:21 2020

@author: bhanvi
"""

import praw
import random
import webbrowser
import sys
import socket


def receive_connection():
    """
    Wait for and then return a connected socket..
    Opens a TCP connection on port 8080, and waits for a single client.
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('localhost', 8080))
    server.listen(1)
    client = server.accept()[0]
    server.close()
    return client


def send_message(client, message):
    """
    Send message to client and close the connection.
    """
    client.send('HTTP/1.1 200 OK\r\n\r\n{}'.format(message).encode('utf-8'))
    client.close()


def main():
    reddit = praw.Reddit(
        client_id= 'O2VsVgcMY3JaUw',
        client_secret= 'LZ14ajDsvPAyS7QXbf6aa9RstTGxrQ',
        user_agent= 'test app1', \
        username = 'flikering_lids007', \
        password = 'Jack@3141' ,\
        redirect_uri='http://localhost:8080',
    )

    try:
        reddit.user.me()
    except Exception as err:
        if (str(err) != 'invalid_grant error processing request'):
            print('LOGIN FAILURE')
        else:
            state = str(random.randint(0, 65000))
            scopes = ['identity', 'history', 'read', 'edit']
            url = reddit.auth.url(scopes, state, 'permanent')
            print('We will now open a window in your browser to complete the login process to reddit.')
            webbrowser.open(url)

            client = receive_connection()
            data = client.recv(1024).decode('utf-8')
            param_tokens = data.split(' ', 2)[1].split('?', 1)[1].split('&')
            params = {key: value for (key, value) in [token.split('=')
                                                    for token in param_tokens]}

            if state != params['state']:
                send_message(client, 'State mismatch. Expected: {} Received: {}'
                            .format(state, params['state']))
                return 1
            elif 'error' in params:
                send_message(client, params['error'])
                return 1

            refresh_token = reddit.auth.authorize(params["code"])
            send_message(client, "Refresh token: {}".format(refresh_token))

            print(refresh_token)
            return 0

if __name__ == "__main__":
    sys.exit(main())




reddit = praw.Reddit(client_id= 'O2VsVgcMY3JaUw', 
                     client_secret= 'LZ14ajDsvPAyS7QXbf6aa9RstTGxrQ', 
                     refresh_token= '585373841541-3eM4UGc3KGz_XlcmjJWjmB1LE__06Q',
                     user_agent='test app1')
import praw
import pandas as pd
import datetime as dt


reddit = praw.Reddit(
    client_id= 'O2VsVgcMY3JaUw', \
    client_secret= 'LZ14ajDsvPAyS7QXbf6aa9RstTGxrQ', \
    user_agent= 'test app1', \
    username = 'flikering_lids007', \
    password = 'Jack@3141')



print(reddit.user.me()) #
subreddit = reddit.subreddit('Nootropics')
top_subreddit = subreddit.top()
top_subreddit = subreddit.top(limit=500)


for submission in subreddit.top(limit=1):
    print(submission.title, submission.id)
    
topics_dict = { "title":[], \
                "score":[], \
                "id":[], \
                "url":[], \
                "comms_num": [], \
                "created": [], \
                "body":[]}
for submission in top_subreddit:
    topics_dict["title"].append(submission.title)
    topics_dict["score"].append(submission.score)
    topics_dict["id"].append(submission.id)
    topics_dict["url"].append(submission.url)
    topics_dict["comms_num"].append(submission.num_comments)
    topics_dict["created"].append(submission.created)
    topics_dict["body"].append(submission.selftext)
    
    
topics_data = pd.DataFrame(topics_dict)

