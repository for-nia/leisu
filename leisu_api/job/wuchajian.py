# coding=utf8

#from selenium import webdriver
#from selenium.webdriver.common.by import By
#webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.settings.userAgent']='Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1'
#webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.settings.Referer']='http://www.zuqiu.me/tv/qqlive41.html'
#driver = webdriver.PhantomJS()
#driver.get('http://w.zhibo.me:8088/qqliveHD41.php')
#print driver.page_source
#print driver.find_elements(By.TAG_NAME,'iframe')
#frame=driver.find_element_by_tag_name('iframe')
#url=frame.get_attribute('src') if frame else driver.find_element_by_tag_name('video').get_attribute('src')
#print url
from bs4 import BeautifulSoup
import requests
import re
import urlparse
header={
    'Referer':'http://www.zuqiu.me/tv/qqlive41.html'
}
url_format='http://w.zhibo.me:8088/qqliveHD{}.php'
def get_line(num):
    url=url_format.format(num)
    res=requests.get(url,headers=header)
    print res.text
    if '404 Not Found' in res.text:
        return
    elif '<video' in res.text:
        return video(res.text)
    else:
        return iframe(res.text)



def iframe(text):
    soup = BeautifulSoup(text)
    tags = soup.find_all('iframe')
    if len(tags) == 0:
        return
    url=urlparse.urlparse(tags[0]['src'])
    return urlparse.parse_qs(url.query)['id'][0]
    #p = re.compile(r'src=((\'|")https?://.*?\.m3u8)(\'|")')
    #m=p.findall(text)
    #if m:
    #    print m
    #    url=urlparse.urlparse(m[0][0])
    #    return urlparse.parse_qs(url.query)['id'][0]


def video(text):
    p = re.compile(r'src=(\'|")(https?://.*?\.m3u8)(\'|")')
    m=p.findall(text)
    if m:
        return m[0][1]

if __name__=='__main__':
    print get_line(22)