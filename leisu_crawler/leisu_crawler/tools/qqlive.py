# coding=utf8

import sys
sys.path.append('..')
from selenium import webdriver
from selenium.webdriver.common.by import By
import urlparse
import sys
from leisu_crawler.items.Match import Channel
import os
service_args = ['--proxy=127.0.0.1:9050','--proxy-type=socks5',]

def change_ip():
    os.system("""(echo authenticate '"hi@tor"'; echo signal newnym; echo \
          quit) | /bin/nc localhost 9051""")

def get_url(num):
    return get_by_channel_name(u'qqliveHd{}'.format(num))
def get_by_channel_name(name):
    webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.settings.userAgent']='Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1'
    webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.referer']='http://www.zuqiu.me/tv/qqlive41.html'
    driver = webdriver.PhantomJS(service_args=service_args)
    change_ip()
    driver.get('http://w.zhibo.me:8088/{}.php'.format(name))
    print driver.page_source
    frames=driver.find_elements(By.TAG_NAME,'iframe')
    print frames
    videos=driver.find_elements(By.TAG_NAME,'video')
    print videos
    url = videos[0].get_attribute('src') if len(videos)>0 else frames[0].get_attribute('src') if len(frames)>0 else ''
    if len(frames)>0:
        url = get_stream(url)
    return url


def get_stream(url):
    #parsed=urlparse.urlparse(url)
    #return urlparse.parse_qs(parsed.query)['id'][0]
    return url.split('?id=')[1]

def add_channel(channel_name):
    channel_found=Channel.objects(channel_name=channel_name)
    if channel_found:
        return
    channel=Channel()
    if u'qqlive' in channel_name:
        channel.pc_stream=get_url(channel_name[6:])
    else:
        channel.pc_stream=get_by_channel_name(channel_name)
    channel.m_stream=channel.pc_stream
    channel.channel_name=channel_name
    channel.c_from='qqlive'
    channel.type='m3u8'
    channel.name=u'QQ直播'+channel_name[6:]
    channel.save()

def refresh_all():
    channels=Channel.objects(c_from='qqlive')
    for channel in channels:
        refresh(channel)

def refresh(channel):
    if u'qqlive' in channel_name:
        pc_stream=get_url(channel_name[6:])
    else:
        pc_stream=get_by_channel_name(channel_name)
    print pc_stream
    m_stream=pc_stream
    channel.update(pc_stream=pc_stream,m_stream=m_stream)

if __name__=='__main__':
    num=1
    if len(sys.argv)>1:
        num=sys.argv[1]
	print get_url(num)
    else:
        refresh_all()
