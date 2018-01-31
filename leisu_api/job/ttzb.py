# coding=utf8
import sys
sys.path.append('..')
from datetime import datetime, timedelta
from common.items.Match import Match
from common.items.Match import Channel
from selenium import webdriver
from selenium.webdriver.common.by import By
import os

service_args = ['--proxy=127.0.0.1:9050','--proxy-type=socks5',]


def start_requests():
    matches=Match.objects(begin_time__lt=datetime.now(),begin_time__gt=datetime.now()-timedelta(hours=3),stream=1,ttzb__gt=0)
    for match in matches:
        stream=get_stream(match.ttzb)
        match.update(m3u8=stream)

def change_ip():
    os.system("""(echo authenticate '"hi@tor"'; echo signal newnym; echo \
          quit) | /bin/nc localhost 9051""")


def get_stream(ttzb):
    webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.settings.userAgent']='Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1'
    driver = webdriver.PhantomJS(service_args=service_args)
    driver.get('http://m.tiantianzhibo.com/channel/{}.html'.format(ttzb))
    frames=driver.find_elements(By.ID,'iframepage')
    if len(frames)<=0:
        return ''
    driver.get(frames[0].get_attribute('src'))
    return driver.find_element_by_id('ckplayer_player').get_attribute('src')

def add_channel(channel_name):
    channel_found=Channel.objects(channel_name=channel_name,u_time=datetime.now())
    if channel_found:
        return
    channel=Channel()
    channel.pc_stream=get_stream(channel_name)
    channel.m_stream=channel.pc_stream
    channel.channel_name=channel_name
    channel.c_from='ttzb'
    channel.type='m3u8'
    channel.name='天天直播'+channel_name[4:]
    channel.u_time=datetime.now()
    channel.save()

def refresh_all():
    change_ip()
    channels=Channel.objects(c_from='ttzb')
    for channel in channels:
        refresh(channel)

def refresh(channel):
    pc_stream=get_stream(channel.channel_name)
    print pc_stream
    if pc_stream:
        m_stream=pc_stream
        channel.update(pc_stream=pc_stream,m_stream=m_stream)

if __name__=='__main__':
    #start_requests()
    refresh_all()
