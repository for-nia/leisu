# coding=utf8
import scrapy
from leisu_crawler.items.Match import Match
import requests
from datetime import datetime
import json
NAME='LeisuMLQ'
class LeisuLiveMatches(scrapy.Spider):
    name = NAME
    start_urls = []
    leisu_img_fmt=u'http://cdn.leisu.com/basketball/teamflag_s/{}'
    session=requests.Session()

    def start_requests(self):
        urls=['http://api.leisu.com/lanqiu/app/live?app=0&lang=0&platform=2&ver=2.5.3']
        #self.parse()
        yield scrapy.Request(urls[0],self.parse)
    
    def parse(self,response):
        #print response.body
        #res=self.session.get('http://api.leisu.com/lanqiu/app/live?app=0&lang=0&platform=2&ver=2.5.3')
        #print res.text
        j=json.loads(response.body)
        mathes=j[u'matches']
        events=j[u'events']
        teams=j[u'teams']
        for match in mathes:
            m = Match()
            if match[2] !=1:continue
            m.match_id=match[0]
            m.league_id=str(match[2])
            m.league_name=events[str(m.league_id)][0]
            m.begin_time=datetime.fromtimestamp(match[4])
            home=match[7]
            m.home_id=str(home[0])
            home_team=teams[str(home[0])]
            m.home_name=home_team[0]
            m.home_head=self.leisu_img_fmt.format(home_team[1])
            m.home_score=sum(home[2:6])
            away=match[6]
            away_team=teams[str(away[0])]
            m.away_id=str(away[0])
            m.away_name=away_team[0]
            m.away_score=sum(away[2:6])
            m.away_head=self.leisu_img_fmt.format(away_team[1])
            m.stream=1
            m.ttzb=0
            m.m_from='leisu'
            m.status=1 if match[3]!=10 else 2
            match_found = Match.objects(match_id=m.match_id)
            print m.home_name.encode('utf-8')+'vs'+m.away_name.encode('utf-8')
            if match_found:
                match_found.update_one(home_score=m.home_score, away_score=m.away_score,stream=m.stream,begin_time=m.begin_time,
                                       upsert=True)
            else:
                m.save()

