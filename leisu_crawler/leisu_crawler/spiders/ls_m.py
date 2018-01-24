# coding=utf8
import scrapy
from leisu_crawler.items.Match import Match
import requests
from datetime import datetime
import time
import json
NAME='LeisuM'
class LeisuLiveMatches(scrapy.Spider):
    name = NAME
    start_urls = []

    fenxi='https://live.leisu.com/shujufenxi-{}/'
    shypeilv='https://live.leisu.com/3in1-{}/'
    oupei='https://live.leisu.com/oupei-{}'
    yapei='https://live.leisu.com/yapan-{}'
    daxiao='https://live.leisu.com/daxiaoqiu-{}'
    statistic_url='https://live.leisu.com/detail-{}'


    leisu_img_fmt='https://cdn.leisu.com/teamflag_s/%s'
    session=requests.Session()

    def start_requests(self):
        urls=['http://api.leisu.com/app/live/live?app=0&lang=0&platform=2&ver=2.6.1']
        yield scrapy.Request(urls[0],callback=self.parse)
    
    def parse(self,response):
        res=self.session.get('http://api.leisu.com/app/live/live?app=0&lang=0&platform=2&ver=2.6.1')
        j=json.loads(res.text)
        mathes=j['matches']
        events=j['events']
        for match in mathes:
            m = Match()
            m.match_id=match[0]
            m.league_id=str(match[1])
            m.league_name=events[str(m.league_id)][0]
            m.begin_time=datetime.fromtimestamp(match[4])
            home=match[5]
            m.home_id=str(home[0])
            m.home_name=home[1]
            m.home_score=home[2]
            away=match[6]
            m.away_id=str(away[0])
            m.away_name=away[1]
            m.away_score=away[2]
            m.home_head , m.away_head = self.headers(m.match_id)
            m.stream=match[10]
            m.ttzb=0
            m.m_from='leisu'
            m.status=1
            match_found = Match.objects(match_id=m.match_id)
            if match_found:
                match_found.update_one(home_score=m.home_score, away_score=m.away_score,stream=m.stream,
                                       upsert=True)
            else:
                m.save()
    
    
    def headers(self,match_id):
        res=self.session.get('http://api.leisu.com/app/live/matchdetail?app=0&k=4b5b53f43cc5674897a133bbd49c5c07&pk=qGE50mjp&platform=2&t=%s&ver=2.6.1&sid=%s'%(int(time.time()),match_id))
        m=json.loads(res.text)
        return self.leisu_img_fmt%m['home'][2],self.leisu_img_fmt%m['away'][2]

