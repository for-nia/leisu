# coding=utf8
import sys
sys.path.append('..')
from datetime import datetime, timedelta
from leisu_crawler.items.Match import Match
from leisu_crawler.items.Match import Channel
from selenium import webdriver
def start_requests():
    matches=Match.objects(begin_time__lt=datetime.now(),begin_time__gt=datetime.now()-timedelta(hours=3),stream=1,ttzb__gt=0)
    for match in matches:
        stream=get_stream(match.ttzb)
        match.update(m3u8=stream)


def get_stream(ttzb):
    webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.settings.userAgent']='Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1'
    driver = webdriver.PhantomJS()
    driver.get('http://m.tiantianzhibo.com/channel/{}.html'.format(ttzb))
    frame=driver.find_element_by_id('iframepage').get_attribute('src')
    driver.get(frame)
    return driver.find_element_by_id('ckplayer_player').get_attribute('src')

def add_channel(channel_name):
    channel_found=Channel.objects(channel_name=channel_name)
    if channel_found:
        return
    channel=Channel()
    channel.pc_stream=get_stream(channel_name)
    channel.m_stream=channel.pc_stream
    channel.channel_name=channel_name
    channel.c_from='ttzb'
    channel.type='m3u8'
    channel.name='天天直播'+channel_name[4:]
    channel.save()

def refresh_all():
    channels=Channel.objects(c_from='ttzb')
    for channel in channels:
        refresh(channel.channel_name)

def refresh(channel):
    pc_stream=get_stream(channel.channel_name)
    m_stream=pc_stream
    channel.update(pc_stream=pc_stream,m_stream=m_stream)

if __name__=='__main__':
    refresh_all()
