
from collections import Counter
import os
import re
import sys
import tweepy

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from tips import add_tips, truncate_tables, get_tips, add_hashtags
from settings import *

def get_tweets(screen_name=TWITTER_ACCOUNT):
    #api = _get_twitter_api_session()
    return tweepy.Cursor(api.user_timeline,
                         screen_name=screen_name,
                         exclude_replies=True,
                         include_rts=False)


def get_hashtag_counter(tips):
    blob = ' '.join(t.text.lower() for t in tips)
    cnt = Counter(TAG.findall(blob))

    if EXCLUDE_PYTHON_HASHTAG:
        cnt.pop('python', None)

    return cnt

def get_favorites():
    return tweepy.Cursor(api.favorites,
                         count=200, 
                         include_entities=True)


def import_tweets(tweets=None):
    if tweets is None:
        tweets = get_tweets(screen_name)
    add_tips(tweets)


def import_hashtags():
    tips = get_tips()
    hashtags_cnt = get_hashtag_counter(tips)
    add_hashtags(hashtags_cnt)



if __name__ == '__main__':
    try:
        screen_name = sys.argv[1]
    except IndexError:
        screen_name = TWITTER_ACCOUNT

    truncate_tables()

    import_tweets()
    import_hashtags()
