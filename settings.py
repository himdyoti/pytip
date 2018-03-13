from collections import Counter
import os
import re
import sys

import tweepy
import plotly.plotly as py


CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_SECRET = os.environ.get('ACCESS_SECRET')
PLOTLY_KEY = os.environ.get('PLOTLY_KEY')
PLOTLY_SECRET = os.environ.get('PLOTLY_SECRET')

TWITTER_ACCOUNT = os.environ.get('PYTIP_APP_TWITTER_ACCOUNT') or 'python_tip'
print(os.environ.get('PYTIP_APP_TWITTER_ACCOUNT'))
EXCLUDE_PYTHON_HASHTAG = True
TAG = re.compile(r'#([a-z0-9]{3,})')

def _get_twitter_api_session():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    return tweepy.API(auth)


api = _get_twitter_api_session()
#py.sign_in(PLOTLY_KEY, PLOTLY_SECRET)
#ptly = py

