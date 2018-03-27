from collections import Counter
import os
import re
import sys

import tweepy
import plotly.plotly as py
from simplecrypt import encrypt, decrypt

CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_SECRET = os.environ.get('ACCESS_SECRET')
PLOTLY_KEY = os.environ.get('PLOTLY_KEY')
PLOTLY_SECRET = os.environ.get('PLOTLY_SECRET')

TWITTER_ACCOUNT = os.environ.get('PYTIP_APP_TWITTER_ACCOUNT') or 'python_tip'
EXCLUDE_PYTHON_HASHTAG = True
TAG = re.compile(r'#([a-z0-9]{3,})')

__all__ = ['User','TWITTER_ACCOUNT','TAG','EXCLUDE_PYTHON_HASHTAG']

class User(object):
	def __init__(self,**kwargs):
		self.api = None

	def _get_twitter_api_session(self):
		"""
        api session logic
		"""
		consumer_key = CONSUMER_KEY
		consumer_secret = CONSUMER_SECRET
		access_token = ACCESS_TOKEN
		access_secret = ACCESS_SECRET
		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_secret)
		self.api = tweepy.API(auth)
		return self.api

	def get_api(self):
		return self._get_twitter_api_session()


#py.sign_in(PLOTLY_KEY, PLOTLY_SECRET)
#ptly = py

