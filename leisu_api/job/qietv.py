# coding=utf8

import sys
sys.path.append('..')
from common.items.Match import Channel
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import time
import json

url_fmt=u'http://live.qq.com/api/h5/room?room_id={}&_={}'
video_fmt=u'http://hls.live.zhibo.tv/8live/{}/index.m3u8'
def get_stream(tv_id):
    session=requests.Session()
    session.proxies={}
    res=session.get(url_fmt.format(tv_id,int(round(time.time() * 1000))),timeout=30)
    j=json.loads(res.text)
    if j['data'] and j['data']['hls_url']:
        return j['data']['hls_url']



def add_channel(channel_name):
    channel_found=Channel.objects(channel_name=channel_name)
    if channel_found:
        return
    channel=Channel()
    channel.pc_stream=get_stream(channel_name[6:])
    channel.m_stream=channel.pc_stream
    channel.channel_name=channel_name
    channel.c_from='qietv'
    channel.type='m3u8'
    channel.name=u'企鹅直播'+channel_name[5:]
    channel.u_time=datetime.now()
    channel.save()
def refresh_all():
    #change_ip()
    channels=Channel.objects(c_from='qietv').order_by('u_time','+a')
    for channel in channels:
		try:
			refresh(channel)
		except:
			pass

def refresh(channel):
    print u'begin parse:{}'.format(channel.channel_name)
    pc_stream=get_stream(channel.channel_name[6:])
    print pc_stream
    if pc_stream:
        m_stream=pc_stream
        channel.update(pc_stream=pc_stream,m_stream=m_stream,u_time=datetime.now())

if __name__=='__main__':
    refresh_all()
    #print get_stream(10044916)
