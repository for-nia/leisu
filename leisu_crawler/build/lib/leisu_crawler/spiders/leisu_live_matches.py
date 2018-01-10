# coding=utf8
import scrapy
import re
from leisu_crawler.items.Match import Match
from leisu_crawler.items.Match import Oupei
from leisu_crawler.items.Match import Yapei
from leisu_crawler.items.Match import Biglittle
from leisu_crawler.items.Match import Sanheyi
from datetime import datetime
import ast
NAME='LeisuLiveMatchers'
class LeisuLiveMatches(scrapy.Spider):
    name = NAME
    start_urls = []

    fenxi='https://live.leisu.com/shujufenxi-{}/'
    shypeilv='https://live.leisu.com/3in1-{}/'
    oupei='https://live.leisu.com/oupei-{}'
    yapei='https://live.leisu.com/yapan-{}'
    daxiao='https://live.leisu.com/daxiaoqiu-{}'
    statistic_url='https://live.leisu.com/detail-{}'


    team_detail_url = 'https://data.leisu.com/team-{}'

    def start_requests(self):
        urls=['http://live.leisu.com/']
        yield scrapy.Request(urls[0],callback=self.parse)

    def parse(self,response):
        games=response.css('.list-item')
        for game in games:
            match_id=game.xpath('.//@data-id').extract()[0]
            begin_time=game.xpath('.//@data-nowtime').extract()[0]
            league=game.xpath('.//div/div/span[@class="lab-events"]')[0]
            league_id=re.compile('//data.leisu.com/zuqiu-(\d+)/').match(league.xpath('.//a//@href').extract()[0]).group(1)
            league_name = league.xpath('.//a//span/text()').extract()[0]
            league_img = re.compile(r'background-image:url\((.*)\);').match(league.xpath('.//span[@class="event-icon"]/@style').extract()[0]).group(1)
            right=game.xpath('.//div/div/span[@class="float-right"]')[0]
            half=right.xpath('.//span[@class="lab-half"]/text()').extract()[0]
            corner_s=right.xpath('.//span[@class="lab-corner"]/span/text()')
            corner = corner_s.extract()[0] if corner_s else '0-0'
            peilv=right.xpath('.//span[@class="lab-sb"]/span')
            yapei=self.parse_match_peilv(peilv[1])
            shy=self.parse_match_peilv(peilv[2])
            score_s=game.xpath('.//div/div/span[@class="float-left position-r w-300"]/span[@class="lab-score color-red"]/span/b/text()')
            score=score_s.extract()[0] if score_s else '0-0'
            [home_score,away_score]=[x if self.is_empty(x) else 0 for x in score.split('-')]
            home_team=game.xpath('.//div/div/span[@class="float-left position-r w-300"]/span[@class="lab-team-home"]/span/span')
            away_team=game.xpath('.//div/div/span[@class="float-left position-r w-300"]/span[@class="lab-team-away"]/span/span')
            [home_yellow_card,home_red_card]=[home_team[1].xpath('.//text()').extract()[0] if len(home_team)>=2 else 0 ,home_team[2].xpath('.//text()').extract()[0] if len(home_team)>=3 else 0]
            [away_red_card,away_yellow_card]=[away_team[0].xpath('.//text()').extract()[0] if len(away_team)>=1 else 0 ,away_team[1].xpath('.//text()').extract()[0] if len(away_team)>=2 else 0]
            print [home_red_card,home_yellow_card,away_yellow_card,away_red_card]
            data={
                'league_id':league_id,
                'league_name':league_name,
                'begin_time':begin_time,
                'league_img':league_img,
                'yapei':yapei,
                'shy':shy,
                'half':half,
                'corner':corner,
                'home_score':home_score,
                'away_score':away_score,
                'home_red_card':home_red_card,
                'home_yellow_card':home_yellow_card,
                'away_red_card':away_red_card,
                'away_yellow_card':away_yellow_card
                }


            yield scrapy.Request(self.fenxi.format(match_id),callback=self.parse_fenxi,meta=data)
            yield scrapy.Request(self.shypeilv.format(match_id),callback=self.parse_peilv)
            yield scrapy.Request(self.yapei.format(match_id),callback=self.parse_yapei)
            yield scrapy.Request(self.statistic_url.format(match_id,callback=self.statistic))
            yield scrapy.Request(self.daxiao.format(match_id),callback=self.parse_daxiao)
            yield scrapy.Request(self.oupei.format(match_id),callback=self.parse_oupei)

    def is_empty(self,str):
        return str and str.strip()



    def parse_match_peilv(self,peilv):
        home=peilv.xpath('.//span[@class="lab-ratel"]/span/span/text()')
        rangqiu=peilv.xpath('.//span[@class="lab-bet-odds"]/span/span/@data-num')
        away=peilv.xpath('.//span[@class="lab-rater"]/span/span/text()')
        return [home.extract()[0] if home else '',rangqiu.extract()[0] if rangqiu else '',away.extract()[0] if away else '']

    def parse_fenxi(self, response):
        league_id=response.meta.get('league_id')
        begin_time=response.meta.get('begin_time')
        league_name=response.meta.get('league_name')
        league_img=response.meta.get('league_img')
        yapei=response.meta.get('yapei')
        shy=response.meta.get('shy')
        half=response.meta.get('half')
        corner=response.meta.get('corner')
        home_score=response.meta.get('home_score')
        away_score=response.meta.get('away_score')
        [home_half,away_half]=[x if self.is_empty(x) else 0 for x in half.split('-')]
        [home_corner,away_corner]=[x if self.is_empty(x)  else 0 for x in corner.split('-')]
        match_id = int(re.compile(r'https://live.leisu.com/shujufenxi-(\d+)').match(response.url).group(1))
        home = response.xpath('//div[@class="team-home"]')[0]
        home_id=home.xpath('.//@data-id').extract()[0]
        home_team_name = home.xpath('.//div[@class="name"]/span/text()').extract()[0]
        home_head = 'http:{}'.format(home.xpath('.//div[@class="team-icon"]/@style').re(r"background-image: url\('(.*)'\)")[0])
        away = response.xpath('//div[@class="team-away"]')[0]
        away_id=away.xpath('.//@data-id').extract()[0]
        away_team_name = away.xpath('.//div[@class="name"]/span/text()').extract()[0]
        away_head = 'http:{}'.format(away.xpath('.//div[@class="team-icon"]/@style').re(r'background-image: url\(\'(.*)\'\)')[0])
        match=Match(match_id=match_id,home_name=home_team_name,home_head=home_head,away_name=away_team_name,away_head=away_head,begin_time=datetime.fromtimestamp(int(begin_time)))
        match.league_id=league_id
        match.league_name=league_name
        match.home_id=home_id
        match.away_id=away_id
        match.league_img=league_img
        match.home_half=int(home_half)
        match.away_half=int(away_half)
        match.home_corner=int(home_corner)
        match.away_corner=int(away_corner)
        match.yapei=yapei
        match.shy=shy
        match.home_score=home_score
        match.away_score=away_score
        match_found=Match.objects(match_id=match_id)
        match.home_red_card=response.meta.get('home_red_card')
        match.home_yellow_card=response.meta.get('home_yellow_card')
        match.away_red_card=response.meta.get('away_red_card')
        match.away_yellow_card=response.meta.get('away_yellow_card')
        match.status=1
        if match_found:match_found.update_one(home_score = home_score, away_score = away_score,
                                              home_half = home_half, away_half = away_half,
                                              home_corner = home_corner, away_corner = away_corner,
                                              upsert=True)
        else:match.save()
        yield scrapy.Request(self.team_detail_url.format(home_id),callback=self.parse_team)
        yield scrapy.Request(self.team_detail_url.format(away_id),callback=self.parse_team)


    def get_shy_list(self,tr):
        first=tr.xpath('.//td/span/text()').extract()
        yield first[0] if len(first)>0 else None
        second=tr.xpath('.//td/text()').extract()
        yield second[0] if len(second)>0 else None
        third = tr.xpath('.//td/span/text()').extract()
        yield third[0] if len(third)>0 else None

    def parse_peilv(self,response):
        match_id = int(re.compile(r'[^\d]*(\d+)').match(response.url).group(1))
        trs = response.xpath('//table[@class="main"]/tbody/tr')
        for tr in trs:
            company = tr.xpath('.//@data-company').extract()[0]
            rangqiu = tr.xpath('.//td[@class="rangQiu"]/table/tbody/tr')[0]
            rq_first = [x for x in self.get_shy_list(rangqiu)]
            rq_current = [x for x in self.get_shy_list(rangqiu)]
            bzp = tr.xpath('.//td[@class="biaoZhunPan"]/table/tbody/tr')[0]
            bzp_first= [x for x in self.get_shy_list(bzp)]
            bzp_current = [x for x in self.get_shy_list(bzp)]
            dxq_rate = tr.xpath('.//td[contains(@class,"daXiaoQiu")]/table/tbody/tr')
            dxq_first = [x for x in self.get_shy_list(dxq_rate)]
            dxq_current = [x for x in self.get_shy_list(dxq_rate)]
            shy=Sanheyi(match_id=match_id,company_id=company,rq_first=rq_first,rq_current=rq_current,bz_first=bzp_first,bz_current=bzp_current,bl_first=dxq_first,bl_current=dxq_current)
            shy_f=Sanheyi.objects(match_id=match_id,company_id=company)
            if shy_f:shy_f.update_one(rq_first=rq_first,rq_current=rq_current,bz_first=bzp_first,bz_current=bzp_current,bl_first=dxq_first,bl_current=dxq_current,upsert=True)
            else:shy.save()



    def parse_oupei(self,response):
        match_id = int(re.compile(r'[^\d]*(\d+)').match(response.url).group(1))
        trs=response.xpath('//table[@class="main"]/tbody/tr')
        for tr in trs:
            company = tr.xpath('.//@data-company').extract()[0]
            peilv = tr.xpath('.//td[@class="peilv"]/table/tbody/tr')
            peilv_first=[x for x in peilv[0].xpath('.//td/span/text()').extract()]
            peilv_current=[x for x in peilv[1].xpath('.//td/span/text()').extract()]
            gailv = tr.xpath('.//td[@class="gailv"]/table/tbody/tr')
            gailv_first = gailv[0].xpath('.//@data-rate').extract()[0]
            gailv_current = gailv[1].xpath('.//@data-rate').extract()[0]
            #print eval(gailv_first)+eval(gailv_current)
            fanhuan = tr.xpath('.//td[contains(@class,"fanhuan")]/@data-rate').extract()[0]
            kelly_rate= tr.xpath('.//td[contains(@class,"kelly")]/table/tbody/tr')
            kelly_first=[x for x in kelly_rate[0].xpath('.//td/span/text()').extract()]
            kelly_current=[x for x in kelly_rate[1].xpath('.//td/span/text()').extract()]
            oupei=Oupei(match_id=match_id,company_id=company,peilv_chupan=peilv_first,peilv_jipan=peilv_current,fanhuan=fanhuan)
            oupei.kelly_chupan=kelly_first
            oupei.kelly_jipan=kelly_current
            oupei.gailv_chupan=gailv_first
            oupei.gailv_jipan=gailv_current
            oupei_found = Oupei.objects(match_id=match_id,company_id=company)
            if oupei_found:oupei_found.update_one(peilv_chupan=peilv_first,peilv_jipan=peilv_current,fanhuan=fanhuan,upsert=True)
            else:oupei.save()


    def parse_yapei(self,response):
        match_id = int(re.compile(r'[^\d]*(\d+)').match(response.url).group(1))
        trs = response.xpath('//table[@class="main"]/tbody/tr')
        for tr in trs:
            company = int(tr.xpath('.//@data-company').extract()[0])
            data_odds = tr.xpath('.//@data-odds').extract()[0]
            time = tr.xpath('.//td[@class="time"]/text()').extract()[0]
            print 'yapei->>>>>'+data_odds
            if '[,,,,,]'==data_odds.replace(' ',''):continue
            yapei=Yapei(match_id=match_id,company_id=company,data_odds=ast.literal_eval(data_odds),last_time=time)
            yapei_found=Yapei.objects(match_id=match_id,company_id=company)
            last_time=datetime.strptime(time,'%Y-%m-%d %H:%M')
            if yapei_found:yapei_found.update_one(data_odds=ast.literal_eval(data_odds),last_time=last_time)
            else:yapei.save()



    def statistic(self,response):
        pass

    def parse_daxiao(self,response):
        match_id = int(re.compile(r'[^\d]*(\d+)').match(response.url).group(1))
        trs=response.xpath('//table[@class="main"]/tbody/tr')
        for tr in trs:
            company=int(tr.xpath('.//@data-company').extract()[0])
            data_odds=tr.xpath('.//@data-odds').extract()[0]
            time=tr.xpath('.//td[@class="time"]/text()').extract()[0]
            if '[,,,,,]'==data_odds.replace(' ',''):continue
            biglittle=Biglittle(match_id=match_id,company_id=company,data_odds=ast.literal_eval(data_odds),last_time=time)
            bl_f=Biglittle.objects(match_id=match_id,company_id=company)
            last_time=datetime.strptime(time,'%Y-%m-%d %H:%M')
            if bl_f:bl_f.update_one(data_odds=ast.literal_eval(data_odds),last_time=last_time)
            else:biglittle.save()

    def parse_team(self,response):
        pass
