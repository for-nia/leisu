# coding=utf8
import sys
sys.path.append('..')
from datetime import datetime, timedelta
from common.items.Match import Match
from common.items.Match import Channel
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import signal
from selenium.common.exceptions import TimeoutException
#import dryscrape
from bs4 import BeautifulSoup
#import webkit_server
import requests
import subprocess
import time
import json
headers = {
'Accept':'application/json, text/javascript, */*; q=0.01',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'en,zh-CN;q=0.9,zh;q=0.8',
'Cache-Control':'no-cache',
'Connection':'keep-alive',
'Cookie':'Hm_lvt_644b49eb7c9bae6b5db3f0b4f3408d8b=1515507860; ha=1; Hm_lpvt_644b49eb7c9bae6b5db3f0b4f3408d8b=1517654210; Hm_lvt_0d1ed7d868c02273358f9071e84eff0e=1517147600,1517147636,1517505758,1517654218; ha=1; Hm_lpvt_0d1ed7d868c02273358f9071e84eff0e=1517655716',
'Host':'m.tiantianzhibo.com',
'Pragma':'no-cache',
'Referer':'http://m.tiantianzhibo.com/channel/ttzb1.html',
'requestKey':'ghl6seMfbp0PmFjSlFja1QkzMYqi8VMZ',
'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1',
'X-Requested-With':'XMLHttpRequest'
}

ip=''
#with open('/tmp/ip','r') as f:ip=f.read().strip()


def start_requests():
    matches=Match.objects(begin_time__lt=datetime.now(),begin_time__gt=datetime.now()-timedelta(hours=3),stream=1,ttzb__gt=0)
    for match in matches:
        stream=get_stream(match.ttzb)
        match.update(m3u8=stream)

def change_ip():
    os.system("""(echo authenticate '"hi@tor"'; echo signal newnym; echo \
          quit) | /bin/nc localhost 9051""")


#def get_stream(ttzb):
#	webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.settings.userAgent']='Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1'
#	ip=open('/tmp/ip','r').read().strip()
#	print u'proxy ip:{}'.format(ip)
#	service_args = ['--proxy=proxy:8128','--proxy-type=https']
#	#service_args = ['--proxy=proxy:8088','--proxy-type=socks5']
#	driver = webdriver.PhantomJS(service_args=service_args)
#	#driver = webdriver.PhantomJS()
#	driver.implicitly_wait(5)
#	driver.set_page_load_timeout(5)
#    #driver = webdriver.PhantomJS()
#	print u'start parse {}'.format(ttzb)
#	try:
#		driver.get('http://m.tiantianzhibo.com/channel/{}.html'.format(ttzb))
#		print driver.page_source
#		frames=driver.find_elements(By.ID,'iframepage')
#		if len(frames)<=0:
#			return ''
#		driver.get(frames[0].get_attribute('src'))
#		src=driver.find_element_by_id('ckplayer_player').get_attribute('src')
#		return src
#	except TimeoutException as e:
#		print e
#		#get_stream(ttzb)
#	finally:
#		driver.service.process.send_signal(signal.SIGTERM)
#		driver.quit()

#def get_stream(ttzb):
#	dryscrape.start_xvfb()
#	server = webkit_server.Server()
#	server_conn = webkit_server.ServerConnection(server=server)
#	driver = dryscrape.driver.webkit.Driver(connection=server_conn)
#	session=dryscrape.Session(driver=driver)
#	session.set_header('user-agent','Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36')
#	session.set_proxy('proxy',8128)
#	session.visit('http://m.tiantianzhibo.com/channel/{}.html'.format(ttzb))
#	soup=BeautifulSoup(session.body())
#	iframe=soup.find('iframe',{'id':'iframepage'})
#	if iframe:
#		session.visit(iframe['src'])
#		soup=BeautifulSoup(session.body())
#		video=soup.find('video')
#		if video:return video['src']
#	server.kill()

def get_stream(ttzb):
    print u'start parse {}'.format(ttzb)
    headers['Referer'] = u'http://m.tiantianzhibo.com/channel/ttzb1.html'.format(ttzb)
    session = requests.Session()
    session.proxies = {'http': 'http://proxy:8128', 'https': 'http://proxy:8128'}
    res = session.get('http://m.tiantianzhibo.com/api/signallist.php?ch={}'.format(ttzb), headers=headers,timeout=3)
    print res.text
    j = json.loads(res.text)
    print j['key']
    r = session.get(u'http://m.tiantianzhibo.com/player.html?ch={}&p=dn&v={}&k={}&w=375&h=251'.format(ttzb,j['default'][0],j['key']),timeout=30)
    #print r.text
    soup = BeautifulSoup(r.text)
    s = soup.findAll('script')
    script = s[1].text
    js = script[:5] + 'console.log(' + script[5:] + ')'
    tmp_file = str(round(time.time()) * 1000) + '.js'
    with open(tmp_file, 'w') as f:
        f.write(js)
    try:
        output = subprocess.check_output("node {}".format(tmp_file), shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
    try:
        os.remove(tmp_file)
    except OSError:
        pass
    tmp_file = str(round(time.time() * 1000)) + '.js'
    with open(tmp_file, 'w') as f:
        f.write(str(output).split('function ckcpt()')[0] + 'console.log(play_url)')
    try:
        output = subprocess.check_output("node {}".format(tmp_file), shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
    try:
        os.remove(tmp_file)
    except OSError:
        pass
    return output.rstrip()


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
    channel.name=u'足球直播'+channel_name[4:]
    channel.u_time=datetime.now()
    channel.save()

def refresh_all():
    #change_ip()
    channels=Channel.objects(c_from='ttzb').order_by('u_time','+a')
    for channel in channels:
		try:
			refresh(channel)
		except:
			pass

def refresh(channel):
    pc_stream=get_stream(channel.channel_name)
    print pc_stream
    if pc_stream:
        m_stream=pc_stream
        channel.update(pc_stream=pc_stream,m_stream=m_stream,u_time=datetime.now())

if __name__=='__main__':
    #start_requests()
    refresh_all()
	#print get_stream('ttzb6')
