# coding=utf8
import sys
sys.path.append('..')
from common.items.Match import Match
import requests
from datetime import datetime
import time
import json
header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en,zh-CN;q=0.8,zh;q=0.6',
    'Cache-Control': 'no-cache',
    'Host': 'api.leisu.com',
    'Pragma': 'no-cache',
    'Proxy-Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}
leisu_img_fmt='https://cdn.leisu.com/teamflag_s/%s'
def parse():
    res = requests.get('http://api.leisu.com/app/live/live?app=0&lang=0&platform=2&ver=2.6.1',headers=header)
    j = json.loads(res.text)
    print res.text
    mathes = j['matches']
    events = j['events']
    for match in mathes:
        m = Match()
        m.match_id = match[0]
        m.league_id = str(match[1])
        m.league_name = events[str(m.league_id)][0]
        m.begin_time = datetime.fromtimestamp(match[4])
        home = match[5]
        m.home_id = str(home[0])
        m.home_name = home[1]
        m.home_score = home[2]
        away = match[6]
        m.away_id = str(away[0])
        m.away_name = away[1]
        m.away_score = away[2]
        m.home_head, m.away_head = headers(m.match_id)
        m.stream = match[10]
        m.ttzb = 0
        match_found = Match.objects(match_id=m.match_id)
        if match_found:
            match_found.update_one(home_score=m.home_score, away_score=m.away_score,
                                   upsert=True)
        else:
            m.save()


def headers():
    res = requests.get(
        'http://api.leisu.com/app/live/matchdetail?app=0&k=4b5b53f43cc5674897a133bbd49c5c07&pk=qGE50mjp&platform=2&t=%s&ver=2.6.1&sid=%s' % (
        int(time.time()), match_id))
    m = json.loads(res.text)
    return leisu_img_fmt % m['home'][2], leisu_img_fmt % m['away'][2]

if __name__=='__main__':
    parse()