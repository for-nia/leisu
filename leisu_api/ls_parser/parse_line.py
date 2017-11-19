# coding=utf8
import requests
import re

headers={
'Host':'www.goallive.tv',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Referer':'http://live.leisu.com/stream-2296625',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'en,zh-CN;q=0.8,zh;q=0.6'
}



def get_rtmp(url):
    r = requests.get(url, headers=headers, allow_redirects=False)
    p=re.compile(r'"(rtmp:.*)"')
    m=p.findall(r.text)
    # print r.text
    if m:
        return m[0]

if __name__=='__main__':
    get_rtmp('http://www.goallive.tv/go?id=3107')
