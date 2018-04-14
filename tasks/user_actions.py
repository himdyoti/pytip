
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
from . import twitter_user
from settings import *
from tips import add_tips, truncate_tables, get_tips, add_hashtags, get_tips_count



def apply_pagination(fn):

    def p_wrapper(clobj, **kargs):

        if not config_pagination:
            assert 'start' in kargs.keys(), "start arg not provided"
            assert kargs['start'] > 0 ,"start value must be greater then 0"
            start, end = kargs['start'], kargs.get('end',0)
            assert start <= end, "start must be >= end"
            end = start + 10 if end == 0 else end
            interval = end - start + 1
            assert interval > 10, "interval must be >= 10"
        else:
            assert all(map( lambda k: k in kargs.keys(), ['offset','limit'])), "offset, limit missing from args"
            assert kargs['offset'] >=0 and kargs['limit'] > 0, "valid offset and limit required for pagination"
            offset, limit = kargs['offset'], kargs['limit']
            start, end, interval = 1, limit, 0

        kargs.update(start=start, end=end, interval=interval)
        return fn(clobj, **kargs)
    return p_wrapper




class twitter_user_actions(twitter_user):
    """
     lowest node User->twitter_user->twitter_user_actions, use it everywhere
    """
    def __init__(self):

        super(twitter_user_actions,self).__init__()

    def like_post(self,id):
        """
        && data._json['favorited'] == True update db with data._json['favourites_count']
        """
        try:
            data = self.api.create_favorite(id)
            if isinstance(data,tweepy.models.Status):
                if hasattr(data,'_json'):  
                    return json.dumps(data._json)
        except tweepy.error.TweepError as e:
            print(e.__dict__)
            if e.__dict__['api_code']==139:
                data = unlike_post(id)
                return data

    def unlike_post(self,id):

        try:
            data = self.api.destroy_favorite(id)
            if isinstance(data,tweepy.models.Status):
                if hasattr(data,'_json'):  # && data._json['favorited'] == False
                    return json.dumps(data._json)
        except tweepy.error.TweepError as e:
            print(e.__dict__)

    def get_my_favorites(self):
        pass
        #api.favorites




class Graph:
    """ Grpah utility class """

    def __init__(self,tw_user):
        self.user = tw_user
        self.pagination = Pagination(page_size=20,total_records=get_tips_count(), url='show_graph')


    @staticmethod
    def prepare_gdata(*args,**kargs):

        graphs = dict(
            data = [
                dict(kargs)
            ],
            layout=dict(
                    title='hover over to see what is about',
                    font="size:10")
        )
        return json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)


    @apply_pagination
    def call_graph(self, **kargs):
        """
        creates graph from twitter data where labels are links 
        https://github.com/plotly/plotlyjs-flask-example
        """
        start, end, interval = kargs['start'], kargs['end'], kargs['interval']
        patt = re.compile(r'\<|\>|&nbsp;|&gt;|&lt;|\"|\'')
        url_pre = '<a href="https://twitter.com/'+TWITTER_ACCOUNT+'/status/{}" >{}</a>'
        fav, links, info = [],[],[]

        if config_pagination:
            tweets = get_tips(tag=None, offset=kargs.get('offset'), limit=kargs.get('limit')) #self.user.get_tweets()
        else:
            tweets = self.user.get_tweets().items(300)

        for i,tw in enumerate(tweets, 1):
            if (start <= i <= end):
                fav.append(tw.favorite_count if hasattr(tw,'favorite_count') else tw.likes)
                tdate = tw.created_at if hasattr(tw, 'created_at') else tw.created
                dt = tdate.strftime('%-d%b%-Y %-I.%-M%p') if isinstance(tdate, datetime.datetime) else i
                tid = tw.tweetid if hasattr(tw, 'tweetid') else tw.id
                links.append(url_pre.format(tid,dt))
                info.append(patt.sub('',tw.text[0:40]))
                start = start + 1
                if start > end:
                    if kargs.get('contineous') and not config_pagination:
                        end += interval
                        yield Graph.prepare_gdata(x=links, y=fav, mode='marker',text=info,type='bar')
                        fav, links, info = [],[],[]
                    else:
                        yield Graph.prepare_gdata(x=links, y=fav, mode='marker',text=info,type='bar')
                        break










