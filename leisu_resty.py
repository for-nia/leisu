from flask import Flask,request
from flask import jsonify
from leisu import parse_stream
import sys

app=Flask(__name__)


@app.route("/hello")
def hello():
    return "hello world"

@app.route('/obtain_url')
def obtain_rul():
    gameId=request.args.get('id')
    url=parse_stream('http://api.leisu.com/api/livestream?sid=%s&type=1'%gameId)
    return jsonify(code=200,result={'url':url})


@app.errorhandler(404)
def page_not_found(e):
    return jsonify(code=-20,result='not found')
if __name__=='__main__':
    port=8989
    if len(sys.argv)>1:
        port = sys.argv[1]
    app.run('0.0.0.0',port)
