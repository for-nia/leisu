# coding=utf8
import scrapy


class Wuchajian(scrapy.Spider):

    name = 'wuchajian'


    def start_requests(self):
        urls = ['http://www.wuchajian.com/']
        yield scrapy.Request(urls[0],callback=self.parse)


    def parse(self, response):
        trs=response.xpath('//tr[@class="against"]')
        for tr in trs:
            tds = tr.xpath('.//td')
            league = tds[1].xpath('.//a');
            league_name = league.xpath('.//text()').extract()[0]
            league_url = league.xpath('.//@href').extract()[0]
            print league_name
            print league_url
            getname = lambda td:td.xpath('.//a/strong/text()').extract()[0]
            title = tds[4].xpath('.//text()').extract()[0] if len(tds)==8 else getname(tds[4])+' vs '+getname(tds[6])
            time = tds[7].xpath('.//@t').extract()[0] if len(tds)==8 else tds[9].xpath('.//@t').extract()[0]
            print title
            print time
            getline = lambda a:[a.xpath('.//@href').extract()[0],a.xpath('.//text()').extract()[0]]
            lines = [getline(a) for a in tds[5].xpath('.//a')] if len(tds)==8 else [getline(a) for a in tds[7].xpath('.//a')]
            for line in lines:
                print line[0]
                print line[1]
