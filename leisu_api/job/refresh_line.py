# coding=utf8
import sys
sys.path.append('..')
import re
from datetime import datetime, timedelta
from common.items.Match import Match
from ls_parser.leisu import parse_stream
from job import ttzb


def start_requests():
    matches=Match.objects(m_from='leisu',begin_time__lt=datetime.now(),begin_time__gt=datetime.now()-timedelta(hours=3),stream=1,status=1)
    for match in matches:
        print match.home_name.encode('utf-8')
        url= parse_stream('http://api.leisu.com/api/livestream?sid=%s&type=1' % match.match_id)
        print url
        if not url:continue
        p=re.compile(r'ttzb(\d+)')
        m=p.findall(url)
        if m:
            num=m[0]
            match.update(channels=['ttzb'+num])
            ttzb.add_channel('ttzb'+str(num))

if __name__=='__main__':
    start_requests()
