# coding=utf8

from selenium import webdriver
from selenium.webdriver.common.by import By
import urlparse
import sys
from common.items.Match import Channel

def get_url(num):
    webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.settings.userAgent']='Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1'
    webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.referer']='http://www.zuqiu.me/tv/qqlive41.html'
    driver = webdriver.PhantomJS()
    driver.get('http://w.zhibo.me:8088/qqliveHD{}.php'.format(num))
    frames=driver.find_elements(By.TAG_NAME,'iframe')
    videos=driver.find_elements(By.TAG_NAME,'video')
    url = videos[0].get_attribute('src') if len(videos)>0 else frames[0].get_attribute('src') if len(frames)>0 else ''
    if len(frames)>0:
        url = get_stream(url)
    return url


def get_stream(url):
    parsed=urlparse.urlparse(url)
    return urlparse.parse_qs(parsed.query)['id'][0]

def add_channel(channel_name):
    channel_found=Channel.objects(channel_name=channel_name)
    if channel_found:
        return
    channel=Channel()
    channel.pc_stream=get_url(channel_name[5:])
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
    pc_stream=get_url(channel.channel_name[5:])
    m_stream=pc_stream
    channel.update(pc_stream=pc_stream,m_stream=m_stream)

if __name__=='__main__':
    num=1
    if len(sys.argv)>1:
        num=sys.argv[1]
    print get_url(num)