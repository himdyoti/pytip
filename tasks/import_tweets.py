
from collections import Counter
import os
import re
import sys
import tweepy

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from tips import add_tips, truncate_tables, get_tips, add_hashtags, get_tips_count
from settings import *

class twitter_user(User):

    def __init__(self):
        super(twitter_user,self).__init__(name='xxx', paswd='yyy')
        self.api = self.get_api()
        self.pagination = Pagination(page_size=30, total_records=get_tips_count(), url='home')

    def get_tweets(self,screen_name=TWITTER_ACCOUNT):
        #api = _get_twitter_api_session()
        return tweepy.Cursor(self.api.user_timeline,
                         screen_name=screen_name,
                         exclude_replies=True,
                         include_rts=False)


    def get_hashtag_counter(self,tips):
        blob = ' '.join(t.text.lower() for t in tips)
        cnt = Counter(TAG.findall(blob))

        if EXCLUDE_PYTHON_HASHTAG:
            cnt.pop('python', None)
            return cnt

    def get_favorites(self):
        return tweepy.Cursor(self.api.favorites,
                         count=200, 
                         include_entities=True)


    def import_tweets(self,tweets=None):
        if tweets is None:
            tweets = self.get_tweets(screen_name)
            add_tips(tweets)


    def import_hashtags(self):
        tips = get_tips()
        hashtags_cnt = self.get_hashtag_counter(tips)
        add_hashtags(hashtags_cnt)



if __name__ == '__main__':

    tw_user = twitter_user()

    try:
        screen_name = sys.argv[1]
    except IndexError:
        screen_name = TWITTER_ACCOUNT

    truncate_tables()

    tw_user.import_tweets()
    tw_user.import_hashtags()
