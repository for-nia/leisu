# coding=utf8

import scrapy
from leisu_crawler.items.Match import Match
from leisu_crawler.items.Match import Channel
import re
from datetime import datetime
from leisu_crawler.tools import ttzb
from leisu_crawler.tools import qqlive

leagues=[u'西甲',u'荷甲',u'法甲',u'意甲',u'英超']
class Wuchajian(scrapy.Spider):
    name = "Wuchajian"

    def start_requests(self):
        urls=['http://www.wuchajian.com/']
        yield scrapy.Request(urls[0],self.parsem)

    def parsem(self, response):
        trs = response.css('tr.against')
        for tr in trs:
            league_name=tr.xpath('.//td[@class="matcha"]/a/text()').extract()[0]
            if league_name!='NBA' and league_name not in leagues:
                continue
            teams=tr.xpath('.//td[@class="teama"]/a/strong/text()').extract()
            print teams[0].encode('utf-8')+'vs'+teams[1].encode('utf-8')
            live_link=tr.xpath('.//td[@class="live_link"]/a/@href').extract()
            match_id=tr.xpath('.//td[@class="live_link"]/@id').extract()[0]
            begin_time=tr.xpath('.//td[@class="tixing"]/@t').extract()[0]
            if not begin_time:return
            #print match_id
            match=Match(match_id=match_id)
            match.home_name=teams[0]
            match.away_name=teams[1]
            match.league_name=league_name
            match.begin_time=datetime.strptime(begin_time,'%Y-%m-%d %H:%M')
            match.m_from='wuchajian'
            match.channels=[]
            match_found=Match.objects(match_id=match_id)
            match.stream=1
            match.status=1
            #print match.away_name + ' vs ' +match.home_name
            if match_found:
                self.handle_channel(live_link,match_found[0])
                self.find_ls_match(match_found[0])
            else:
                if match.league_name == 'NBA':
                    match.save()
                    self.handle_channel(live_link,match)
                elif match.league_name in leagues:
                    m=self.find_ls_match(match)
                    if m:self.handle_channel(live_link,m)


    def find_ls_match(self,match):
        #print match.away_name+'+++'+match.home_name
        matches = Match.objects(begin_time=match.begin_time)
        if len(matches)<=0:return
        for m_ls in matches:
            if match.home_name==m_ls.home_name or match.home_name == m_ls.away_name or match.away_name == m_ls.home_name or match.away_name==m_ls.away_name:
                print 'matched'
                print match.away_name.encode('utf-8') + ' vs ' +match.home_name.encode('utf-8')
                m_ls.update(wcj_id=str(match.match_id),stream=1,upsert=True)
                return m_ls


    def handle_channel(self,links,match):
        for link in links:
            channel_name=''
            if 'qqlive' in link:
                m=re.findall(r'qqlive\d+',link)
                channel_name=m[0]
            elif 'ttzb' in link:
                m=re.findall(r'ttzb\d+',link)
                channel_name=m[0]
            elif 'cctv5MD' in link:
                channel_name='cctv5MD'
            elif 'cctv5jia' in link:
                channel_name='cctv5jia'
            elif 'cctv5SD' in link:
                channel_name='cctv5SD'
            elif 'cctv5' in link:
                channel_name='cctv5'

            if channel_name:
                if channel_name in match.channels:
                    self.check_channel(channel_name)
                else :
                    match.channels.append(channel_name)
                    match.update(channels=match.channels)
                    self.check_channel(channel_name)

    def check_channel(self,channel_name):
        channels=Channel.objects(channel_name=channel_name)
        if len(channels)>0:
            return
        self.add_channel(channel_name)

    def add_channel(self,channel_name):
        if 'ttzb' in channel_name:
            ttzb.add_channel(channel_name)
        elif 'qqlive' in channel_name:
            qqlive.add_channel(channel_name)
