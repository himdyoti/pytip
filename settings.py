from collections import Counter
import os
import re
import sys

import tweepy
import plotly.plotly as py
from simplecrypt import encrypt, decrypt
from collections import namedtuple

CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_SECRET = os.environ.get('ACCESS_SECRET')
PLOTLY_KEY = os.environ.get('PLOTLY_KEY')
PLOTLY_SECRET = os.environ.get('PLOTLY_SECRET')

TWITTER_ACCOUNT = os.environ.get('PYTIP_APP_TWITTER_ACCOUNT') or 'python_tip'
EXCLUDE_PYTHON_HASHTAG = True
TAG = re.compile(r'#([a-z0-9]{3,})')

config_pagination = True

__all__ = ['User','TWITTER_ACCOUNT','TAG','EXCLUDE_PYTHON_HASHTAG', 'Pagination', 'config_pagination']

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



class Pagination:
    """Pagination utility class"""

    def __init__(self,**kargs):
        assert kargs['page_size'] , "page_size required"
        assert kargs.get('total_records') != None , "total_records required"
        assert kargs.get('total_records') > kargs.get('page_size') , "page size > total_records"
        self.page_size = kargs['page_size']
        self.total_records = kargs['total_records'] #get_tips_count()
        self.page_no = 1
        self.url = kargs.get('url','home')


    def get_pages(self):
        "pagination for tips graph"
        page_data = namedtuple('page_data','tpages remainder psize')
        tpages, remainder = divmod(self.total_records,self.page_size) if self.total_records > self.page_size else (1,0)
        self.page_data = page_data(tpages=tpages, remainder=remainder, psize=self.page_size)
        return self.page_data

    def get_html_pagination(self,pageno,**kargs):
        self.set_pageno(int(pageno))
        if kargs.get('url'):
            self.url = kargs.get('url')

        tpages, remainder, psize = self.get_pages()
        tpages = tpages + 1 if remainder else tpages
        q_stringChar = '&' if self.url.find('?') > -1 else '?'
        for pageno in range(1,tpages+1):
            offset, limit = self.get_page_range(pageno)
            if self.page_no == pageno:
                html_pagno = '<span class=page_no href={}{}page={}>{}</span>'
            else:
                html_pagno = '<a class="page_no" href="{}{}page={}">{}</a>'
            html_pagno = html_pagno.format(self.url, q_stringChar, pageno, pageno)
            yield html_pagno


    def set_page_size(self,page_size):
        self.page_size = page_size

    def set_pageno(self,pageno):
        self.page_no = pageno

    def get_page_range(self,pageno):
        """
        return startlimit,offset
        """
        pages, remainder, psize = self.get_pages()

        pg_no = int(pageno)
        if 0 < pg_no <= pages:
            return ((pg_no -1) * psize, psize)
        if remainder and pg_no == pages + 1:
            offset, limit = (pg_no -1) * psize, remainder
            return (offset, limit)


#py.sign_in(PLOTLY_KEY, PLOTLY_SECRET)
#ptly = py

