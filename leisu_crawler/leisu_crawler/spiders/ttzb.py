# coding=utf8

import scrapy
from datetime import datetime,timedelta
from leisu_crawler.items.Match import Match
import requests

class Ttzb(scrapy.Spider):
	name=u'ttzb'
	def start_requests(self):
		yield scrapy.Request('http://www.tiantianzhibo.com/',callback=self.parse)

	def parse(self,response):
#		datelist=response.css('div.datelist')
#		for date in datelist:
#			date=date.css.('div.dateheader').extract()[0]
#			m=re.compile(r'(\d+)').findall(date)
			
		zq=response.xpath('//ul[contains(@class,"zuqiu")]')
		for z in zq:
			title=z.xpath('.//li[@class="t4"]/a/text()').extract()
			#lines=z.xpath('.//li[@class="t5"]/a/@href').extract()
			#lines=z.xpath('.//li[@class="t5"]/a/@href').re(r'(ttzb\d+)')
			lines=z.xpath('.//li[@class="t5"]/a/@href')
			day=lines.re(r'(\d{8})')
			line=lines.re(r'(ttzb\d+)')
			if title and line and day:
				time=datetime.strptime(day[0]+' '+z.xpath('.//li[@class="t1"]/text()').extract()[0],'%Y%m%d %H:%M')
				matches=Match.objects(begin_time__gt=time-timedelta(minutes=5),begin_time__lt=time+timedelta(minutes=5))
				for match in matches:
					if match.home_name in title[0] or match.away_name in title[0]:
						print title[0].encode('utf-8')
						if not line[0] in match.channels:
							match.channels.append(line[0])
							match.update(channels=match.channels)
						requests.get('http://localhost:8989/add_channel?channel_name='+line[0])
