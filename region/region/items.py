# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RegionItem(scrapy.Item):
    adCode = scrapy.Field()
    name = scrapy.Field()
    py = scrapy.Field()
    initial = scrapy.Field()
    level = scrapy.Field()
    short_name = scrapy.Field()
    parent = scrapy.Field()
