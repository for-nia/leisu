import sys
sys.path.append('..')
from time import time

from flask import Flask, request
from flask import jsonify
from flask import render_template
from leisu_api.ls_parser.leisu import parse_stream
import json
from datetime import datetime,timedelta
from flask_cors import CORS
import re
from common.items.Match import Match,Channel

app=Flask(__name__,static_folder='static')
CORS(app)
#app.config['JSON_AS_ASCII'] = False

@app.route("/hello")
def hello():
    return "hello world"

@app.route('/obtain_url')
def obtain_rul():
    gameId=request.args.get('id')
    url= parse_stream('http://api.leisu.com/api/livestream?sid=%s&type=1' % gameId)
    return jsonify(code=0,result={'url':url})

@app.route('/leisu/ws',methods=['get','post'])
def leisu_ws():
    #print request.headers
    r_json=request.get_json()
    data=json.loads(r_json)
    #print data
    route=data['route']
    if route=='onScore':
        body=data['body']
        for l in body['data']:
            print l
            match_id=l[0]
            type=l[1]
            refresh_state(match_id,type,l[2],l[3])
    return jsonify(code=0)

def refresh_state(match_id,type,home_scores,away_scores):
    status = 2 if type==8 else 1
    Match.objects(match_id=match_id).update_one(status=status,
                                                home_score=home_scores[0],
                                                home_red_card=home_scores[2],
                                                home_yellow_card=home_scores[3],
                                                home_corner=home_scores[4],
                                                away_score=away_scores[0],
                                                away_red_card=away_scores[2],
                                                away_yellow_card=away_scores[3],
                                                away_corner=away_scores[4])

@app.route('/matches')
def matches():
    page=int(request.args.get('page',0))
    pageSize=int(request.args.get('pageSize',20))
    matches = Match.objects(status=1).order_by('begin_time','a+').skip(page*pageSize).limit(pageSize)  #
    return jsonify(code=0,result={'matches':[m.to_mongo() for m in matches]})


@app.route('/main.html')
def main2():
    match=Match.objects(begin_time__gt=datetime.now()-timedelta(hours=3),stream=1).order_by('begin_time','+a')
    return render_template('main.html',matches=match)

@app.route('/')
def index():
    match=Match.objects(status=1,begin_time__gt=datetime.now()-timedelta(hours=3),stream=1).order_by('begin_time','+a')
    return render_template('main.html',matches=match)

@app.route('/m')
def m_index():
    match=Match.objects(status=1,begin_time__gt=datetime.now()-timedelta(hours=3),stream=1).order_by('begin_time','+a')
    return render_template('m/main.html',matches=match)

@app.route('/player.html')
def player():
    gameId=request.args.get('id')
    match=Match.objects(match_id=gameId)[0]
    for c in match.channels:
        print c
    print match.flv
    if match.flv:
        print match.flv
        return render_template('player.html',match=match)
    else:
        channel_name=request.args.get('channel')
        print channel_name
        channels=Channel.objects(channel_name__in=match.channels)
        print channels
        #channel = channels[0] if len(channels)>0 else None
        #print channel
        #if not channel or (not channel.pc_stream and not channel.m_stream):
        #    channel=Channel() if not channel else channel
        #    channel.pc_stream = parse_stream('http://api.leisu.com/api/livestream?sid=%s&type=1' % gameId)
        channel = None if not channels else channels[match.channels.index(channel_name) if channel_name in match.channels else 0]
        return render_template('player.html',channels=channels,match=match,channel=channel)

@app.route('/leisu')
def leisu():
    #match=Match.objects(begin_time__gt=datetime.datetime.now())
    match=Match.objects()
    return render_template('leisu.html',matches=match)

@app.route('/get_all')
def get_all():
    start=int(time())
    all = leisu.get_html();
    print int(time())-start
    return jsonify(code=0, result={'urls': [{'id': id, 'url': url,'home':home,'away':away} for id, url,home,away in all]})

@app.errorhandler(404)
def page_not_found(e):
    return jsonify(code=-20,result='not found')

@app.route('/refresh_line')
def start_requests():
    matches=Match.objects(begin_time__lt=datetime.now(),begin_time__gt=datetime.now()-timedelta(hours=3),ttzb=0)
    for match in matches:
        url= parse_stream('http://api.leisu.com/api/livestream?sid=%s&type=1' % str(match.match_id))
	print url
	if url:
            p=re.compile(r'ttzb(\d+)')
            m=p.findall(url)
            if m:
                match.update(ttzb=m[0])
    return jsonify(code=0,result='ok')

def run(port=8989):
    app.run('0.0.0.0',port,threaded=True)

if __name__=='__main__':
    port=8989
    if len(sys.argv)>1:
        port = sys.argv[1]
    app.run('0.0.0.0',port,threaded = True)
