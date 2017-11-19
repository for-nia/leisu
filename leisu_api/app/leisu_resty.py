import sys
from time import time

from flask import Flask, request
from flask import jsonify
from flask import render_template
from leisu_api.ls_parser import leisu
import json
import datetime

from leisu_crawler.leisu_crawler.items.Match import Match

app=Flask(__name__)
#app.config['JSON_AS_ASCII'] = False

@app.route("/hello")
def hello():
    return "hello world"

@app.route('/obtain_url')
def obtain_rul():
    gameId=request.args.get('id')
    url= leisu.parse_stream('http://api.leisu.com/api/livestream?sid=%s&type=1' % gameId)
    return jsonify(code=0,result={'url':url})

@app.route('/leisu/ws',methods=['get','post'])
def leisu_ws():
    #print request.headers
    r_json=request.get_json()
    data=json.loads(r_json)
    route=data['route']
    if route=='onScore':
        body=data['data']
        for l in body:
            match_id=l[0]
            type=l[1]
            match=Match.objects(match_id=match_id).first()
            events=[match.home_score,match.home]

@app.route('/index.html')
def index():
    match=Match.objects().order_by('begin_time','+a').skip(10).limit(20)#begin_time__gt=datetime.datetime.now())
    return render_template('index.html',matches=match)
    #return render_template('index.html',matches=[a for a in [{'home_name':'1111','away_name':'222'}]]);
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


def run(port=8989):
    app.run('0.0.0.0',port)

if __name__=='__main__':
    port=8989
    if len(sys.argv)>1:
        port = sys.argv[1]
    app.run('0.0.0.0',port)
