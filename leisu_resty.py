from flask import Flask,request
from flask import jsonify
import leisu
import sys

app=Flask(__name__)


@app.route("/hello")
def hello():
    return "hello world"

@app.route('/obtain_url')
def obtain_rul():
    gameId=request.args.get('id')
    url=leisu.parse_stream('http://api.leisu.com/api/livestream?sid=%s&type=1'%gameId)
    return jsonify(code=0,result={'url':url})


@app.route('/get_all')
def get_all():
    all = leisu.get_html();
    return jsonify(code=0, result={'urls': [{'id': id, 'url': url,'home':home,'away':away} for id, url,home,away in all]})

@app.errorhandler(404)
def page_not_found(e):
    return jsonify(code=-20,result='not found')
if __name__=='__main__':
    port=8989
    if len(sys.argv)>1:
        port = sys.argv[1]
    app.run('localhost',port)
