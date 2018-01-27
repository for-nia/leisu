# coding=utf8
import sys
sys.path.append('..')
from common.items.Match import Match
import requests
import json
from datetime import datetime,timedelta
def refresh():
    matches=Match.objects(begin_time__lt=datetime.now(),begin_time__gt=datetime.now()-timedelta(hours=3),m_from='leisu')
    for match in matches:
        status = get_status(match.match_id)
        if status > 9:
            print match.match_id
        if status==8:
            match.update(status=2,upsert=True)

def get_status(match_id):
    res=requests.get('http://api.leisu.com/app/live/matchdetail?app=0&k=4b5b53f43cc5674897a133bbd49c5c07&pk=qGE50mjp&platform=2&t=%s&ver=2.6.1&sid={}'.format(match_id))
    j=json.loads(res.text)
    return j['status']

if __name__=='__main__':
    refresh()
