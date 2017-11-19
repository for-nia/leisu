# coding utf8

import websocket
import requests
import re
import time
import ssl
import thread

def get_uri():
    url='http://push.leisu.com/socket.io/1/?t=%d'%long(time.time())+'76'
    res=requests.get(url)
    m=re.compile(r'(\w+):').findall(res.text)
    if m:
        return m[0]

def on_message(ws, message):
    print('onMessage---->'+message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        for i in range(3):
            time.sleep(1)
        time.sleep(1)
        ws.close()
        print("thread terminating...")
    thread.start_new_thread(run, ())

if __name__ == "__main__":
    websocket.enableTrace(True)
    url = "wss://push.leisu.com/socket.io/2/{}".format(get_uri())
    print url
    ws = websocket.WebSocketApp(url,
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
