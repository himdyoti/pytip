import os

from bottle import route, run, request, static_file, view, template
from settings import *
from tips import get_hashtags, get_tips
from tips.db import session
from tasks import *
from tasks.user_actions import *


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
    likes = get_favorites()
    likes = [like.id for like in likes.items(200)]
    

    return {'search_tag': tag or '',
            'tags': tags,
            'tips': tips,
            'screen': TWITTER_ACCOUNT,
            'likes': likes}

@route('/like_a_post', method='POST')
def like_a_post():
    tid = request.POST.get('id', None)
    action = request.query.get('action', None)
    if tid: 
        json_data = like_post(tid) if action == 'nolike' else unlike_post(tid)
        return json_data

@route('/show_graph')
@view('graph')
def show_graph():
    try:
        start = int(request.query.get('start', 0))
        end = int(request.query.get('end', 0))
        data = call_graph(start,end)
        print(data)
        return { 'graphData':data}

    except ValueError:
        return "integer type cast error"
        #return data



if os.environ.get('APP_LOCATION') == 'heroku':
    run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
else:
    run(host='localhost', port=8081, debug=True, reloader=True)

