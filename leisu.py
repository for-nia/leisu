# coding utf8

import requests
import json
from bs4 import BeautifulSoup
import parse_line
import re

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en,zh-CN;q=0.8,zh;q=0.6',
    'Cache-Control': 'no-cache',
    'Host': 'api.leisu.com',
    'Origin': 'http://live.leisu.com',
    'Pragma': 'no-cache',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://live.leisu.com/stream-2292575',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'Cookie':'Hm_lvt_c6b2d49f4c05828df5b14e5c672c37d2=1508848773; Hm_lpvt_c6b2d49f4c05828df5b14e5c672c37d2=1508848773'
}

def parse_stream(url):
    #r=requests.get('http://api.leisu.com/api/livestream?sid=2292731&type=1',headers=headers)
    headers['Referer']=url
    r=requests.get(url,headers=headers)
    # print r.text
    data=json.loads(r.text)
    # print data
    if 'url' in data:
        url = data['url']
        if 'pc' in url:
            print 'url:%s'%url['pc']
            parse_line.get_rtmp(url['pc'])

def get_html():
    streams=requests.get('https://live.leisu.com/')
    soup=BeautifulSoup(streams.text)
    for a in soup.select('a.icon-liveanimation'):
        #parse_stream('http:'+a['href'])
        parse_stream('http://api.leisu.com/api/livestream?sid=%s&type=1'%get_stream_id('http:'+a['href']))

def get_stream_id(url):
    pattern=re.compile(r'http://live\.leisu\.com/stream-(\d+)')
    matcher=pattern.match(url)
    if matcher:
        return matcher.group(1)

if __name__=='__main__':
    get_html()
    #print get_stream_id('http://live.leisu.com/stream-2292731')