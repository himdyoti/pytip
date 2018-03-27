from collections import namedtuple, Counter

from tasks import twitter_user

tip = namedtuple('Tip', 'text')

tw_user = twitter_user()
def test_get_hashtag_counter():
    blob = '''a lot of tweets with #jupyter hashtags, some #python, more
              #itertools, ah and of course lot of #numpy #NUMpy #NumPY
              #pandas is our favorite we got tons of that #pandas #pandas
              #pandas ok do some more #pandas and #jupyter and #python3'''
    tips = blob.split(',')
    tips = [tip(text=t) for t in tips]
    expected = Counter({'pandas': 5,
                        'numpy': 3,
                        'jupyter': 2,
                        'itertools': 1,
                        'python3': 1})
    assert tw_user.get_hashtag_counter(tips) == expected
