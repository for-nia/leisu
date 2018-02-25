# coding=utf8

import sys
sys.path.append('..')
from common.items.Match import Channel
from datetime import datetime
import requests
from bs4 import BeautifulSoup

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en,zh-CN;q=0.8,zh;q=0.6',
    'Cache-Control': 'no-cache',
    'Cookie': 'PHPSESSID=t055lvtd10d2fj9p67rdq2j0f5; js_session_id=t055lvtd10d2fj9p67rdq2j0f5; Hm_lvt_6a1d4f18f62d602b7b3d95df38e345e7=1517800890; Hm_lpvt_6a1d4f18f62d602b7b3d95df38e345e7=1517801110',
    'Host': 'www.zhibo.tv',
    'Pragma': 'no-cache',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://www.zhibo.tv/index/index',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Mobile Safari/537.36'
}
url_fmt=u'http://www.zhibo.tv/m/{}'
video_fmt=u'http://hls.live.zhibo.tv/8live/{}/index.m3u8'
def get_stream(tv_id):
    session=requests.Session()
    session.proxies={}
    res=session.get(url_fmt.format(tv_id),headers=headers,timeout=30)
    soup = BeautifulSoup(res.text)
    room_info = soup.find('input',{'id':'roomInfo'})
    if room_info:
        return room_info['hls_poll_url']+room_info['video_stream']+room_info['hls_default_source']



def add_channel(channel_name):
    channel_found=Channel.objects(channel_name=channel_name)
    if channel_found:
        return
    channel=Channel()
    channel.pc_stream=get_stream(channel_name[8:])
    channel.m_stream=channel.pc_stream
    channel.channel_name=channel_name
    channel.c_from='zhibotv'
    channel.type='m3u8'
    channel.name=u'体育直播'+channel_name[7:]
    channel.u_time=datetime.now()
    channel.save()

if __name__=='__main__':
    print get_stream(30241768)
