# coding=utf8
import sys
sys.path.append('..')
import re
from datetime import datetime, timedelta
from common.items.Match import Match
from ls_parser.leisu import parse_stream
from job import ttzb


def start_requests():
    matches=Match.objects(m_from='leisu',begin_time__lt=datetime.now()+timedelta(minutes=10),begin_time__gt=datetime.now()-timedelta(hours=3),stream=1,status=1)
    for match in matches:
        print match.home_name.encode('utf-8')
        url= parse_stream('http://api.leisu.com/api/livestream?sid=%s&type=1' % match.match_id)
        print url
        if not url:continue
        p=re.compile(r'ttzb(\d+)')
        m=p.findall(url)
        if m:
            num=m[0]
            line=u'ttzb{}'.format(num)
            if not line in match.channels:
                match.channels.append(line)
                match.update(channels=match.channels)
                ttzb.add_channel('ttzb'+str(num))
        elif 'flv' in url:
            match.update(flv=url)

if __name__=='__main__':
    start_requests()
