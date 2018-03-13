
from collections import Counter
import os
import re
import sys
from collections import namedtuple
import datetime
import json
from bottle import run, template, get, post, request
import tweepy
import plotly
from plotly.graph_objs import *

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from . import get_tweets
from settings import *


def like_post(id):
    """
    && data._json['favorited'] == True update db with data._json['favourites_count']
    """
    try:
        data = api.create_favorite(id)
        if isinstance(data,tweepy.models.Status):
            if hasattr(data,'_json'):   # 
                                        # 
                return json.dumps(data._json)
    except tweepy.error.TweepError as e:
    	print(e.__dict__)
    	if e.__dict__['api_code']==139:
    	    data = unlike_post(id)
    	    return data

def unlike_post(id):

    try:
        data = api.destroy_favorite(id)
        if isinstance(data,tweepy.models.Status):
            if hasattr(data,'_json'):  # && data._json['favorited'] == False
                return json.dumps(data._json)
    except tweepy.error.TweepError as e:
        print(e.__dict__)

def get_my_favorites():
	pass
	#api.favorites

def call_graph(start=0, end=0):
    """
    creates graph from twitter data where labels are links 
    """

    end = start + 10 if end is 0 else end
    if start and start <= end:
        patt = re.compile(r'\<|\>|&nbsp;|&gt;|&lt;|\"|\'')
        url_pre = '<a href="https://twitter.com/'+TWITTER_ACCOUNT+'/status/{}" >{}</a>'
        fav = []
        links = []
        info = []
        tweets = get_tweets()
        for i,tw in enumerate(tweets.items(200), 1):
            if (i >= start) and (start <= end)  and (i <= end):
                fav.append(tw.favorite_count)
                dt = tw.created_at.strftime('%-d%b%-Y %-I.%-M%p') if isinstance(tw.created_at, datetime.datetime) else i
                links.append(url_pre.format(tw.id,dt))
                info.append(patt.sub('',tw.text[0:40]))
                start = start + 1
                if start > end:
                    break

        graphs = dict(
            data = [
              dict(
                  x=links,
                  y=fav,
                  mode = 'marker',
                  text= info,
                  type= 'bar'
               ),

            ],
            layout = dict(title='hover over to see what is about')
        )
        return json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)







