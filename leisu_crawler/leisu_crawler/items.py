# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LeisuCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Match(scrapy.Item):
    home_name=scrapy.Field()
    home_head=scrapy.Field()
    away_name=scrapy.Field()
    away_head=scrapy.Field()
    begin_time=scrapy.Field()
