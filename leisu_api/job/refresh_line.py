# coding=utf8
import sys
import re
from datetime import datetime, timedelta
from Match import Match
from leisu import parse_stream


def start_requests():
    matches=Match.objects(begin_time__lt=datetime.now(),begin_time_gt=datetime.now()-timedelta(hours=3),ttzb=0)
    for match in matches:
        url= parse_stream('http://api.leisu.com/api/livestream?sid=%s&type=1' % matches.match_id)
        p=re.compile(r'ttzb(\d+)')
        m=p.findall(url)
        if m:
            match.update(ttzb=m[0])

if __name__=='__main__':
    start_requests()