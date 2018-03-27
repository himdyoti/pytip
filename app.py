import os

from bottle import route, run, request, static_file, view, template
from settings import *
from tips import get_hashtags, get_tips
from tips.db import session
from tasks import *
from tasks.user_actions import twitter_user_actions
tw_user_action = twitter_user_actions()

@route('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root='static')


@route('/')
@route('/<tag>')
@view('index')
def index(tag=None):
    tag = tag or request.query.get('tag') or None
    tags = get_hashtags()
    tips = get_tips(tag)
    likes = tw_user_action.get_favorites()
    likes = [like.id for like in likes.items(200)]
    

    return {'search_tag': tag or '',
            'tags': tags,
            'tips': tips,
            'likes': likes,
            'screen': TWITTER_ACCOUNT
            }

@route('/like_a_post', method='POST')
def like_a_post():
    tid = request.POST.get('id', None)
    action = request.query.get('action', None)
    if tid: 
        json_data = tw_user_action.like_post(tid) if action == 'nolike' else tw_user_action.unlike_post(tid)
        return json_data

@route('/show_graph')
@view('graph')
def show_graph():
    try:
        start = int(request.query.get('start', 0))
        end = int(request.query.get('end', 0))
        data = tw_user_action.call_graph(start,end)
        return { 'graphData':data}

    except ValueError:
        return "integer type cast error"



if os.environ.get('APP_LOCATION') == 'heroku':
    run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
else:
    run(host='localhost', port=8081, debug=True, reloader=True)

