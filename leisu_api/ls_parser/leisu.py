# coding utf8

import json
import re

import requests
from bs4 import BeautifulSoup

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

stream_headers={
'Host':'www.goallive.tv',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Referer':'http://live.leisu.com/stream-2296625',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'en,zh-CN;q=0.8,zh;q=0.6'
}

session=requests.Session()
session.proxies={'http': 'http://proxy:8128', 'https': 'http://proxy:8128'}


def get_rtmp(url):
    r = session.get(url, headers=stream_headers, allow_redirects=False,timeout=10)
    p=re.compile(r'"(rtmp:.*)"|"(http:.*)"')
    #print r.text
    m=p.findall(r.text)
    # print r.text
    #print m
    if m and m[0]:
            return m[0][0] if m[0][0] else m[0][1]

def parse_stream(url):
    #r=requests.get('http://api.leisu.com/api/livestream?sid=2292731&type=1',headers=headers)
    headers['Referer']=url
    r=session.get(url,headers=headers,timeout=10)
    data=json.loads(r.text)
    print r.text
    if 'url' in data:
        url = data['url']
        if 'pc' in url:
            return get_rtmp(url['pc'])

def get_html():
    streams=session.get('https://live.leisu.com/')
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
    print parse_stream(u'http://api.leisu.com/api/livestream?sid={}&type=1'.format(2433533))
