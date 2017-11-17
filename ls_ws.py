# coding=utf8
import websocket
import thread
import time
import requests
import re
import json

def get_uri():
    url='http://push.leisu.com/socket.io/1/?t=%d'%long(time.time()*100)
    res=requests.get(url)
    m=re.compile('[^:]+').findall(res.text)
    if m:
        return m[0]

def on_message(ws, message):
    if(message == ''.join(chr(i) for i in [49, 58, 58])):
        j = {
            "topic": "inplay",
            "timestamp": long(time.time()*100)
        }
        ws.send(''.join(chr(i) for i in [51, 58, 58, 58, 00, 00, 00, 02, 28])+'connector.entryHandler.enter'+json.dumps(j))
    elif message == ''.join(chr(i) for i in [50, 58, 58]):
        ws.send(message)
    print 'msg---->'+message.decode('utf-8').encode('gb18030')

def on_error(ws, error):
    print 'onError----'
    print error

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    # def run(*args):
    #     for i in range(3):
    #         time.sleep(1)
    #         ws.send("Hello %d" % i)
    #     time.sleep(1)
    #     ws.close()
    #     print("thread terminating...")
    # thread.start_new_thread(run, ())
    pass

def on_connect(ws):
    print 'connect'


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://push.leisu.com/socket.io/1/websocket/" + get_uri(),
                                header={'Origin': 'https://live.leisu.com', 'Referer': 'https://live.leisu.com/'},
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close,
                                on_open=on_connect)
    ws.on_open = on_open
    ws.run_forever()
