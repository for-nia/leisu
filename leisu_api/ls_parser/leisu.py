# coding utf8

import json
import re

import requests
from bs4 import BeautifulSoup

import parse_line

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
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}

def parse_stream(url):
    #r=requests.get('http://api.leisu.com/api/livestream?sid=2292731&type=1',headers=headers)
    headers['Referer']=url
    r=requests.get(url,headers=headers)
    data=json.loads(r.text)
    print r.text
    if 'url' in data:
        url = data['url']
        if 'pc' in url:
            return parse_line.get_rtmp(url['pc'])

def get_html():
    streams=requests.get('https://live.leisu.com/')
    soup=BeautifulSoup(streams.text)
    for a in soup.select('a.icon-liveanimation'):
        stream_id = get_stream_id('http:'+a['href'])
        home = get_home_name(a)
        away = get_away_name(a)
        url = parse_stream('http://api.leisu.com/api/livestream?sid=%s&type=1'%stream_id)
        if(url):
            yield stream_id,url,home,away

def get_home_name(a):
    return a.parent.parent.parent.select('span.lab-team-home')[0].find('a').text


def get_away_name(a):
    return a.parent.parent.parent.select('span.lab-team-away')[0].find('a').text

def get_stream_id(url):
    pattern=re.compile(r'http://live\.leisu\.com/stream-(\d+)')
    matcher=pattern.match(url)
    if matcher:
        return matcher.group(1)

if __name__=='__main__':
    #get_html()
    print parse_stream(u'http://api.leisu.com/api/livestream?sid={}&type=1'.format(2226817))
