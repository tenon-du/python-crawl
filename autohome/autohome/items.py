# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# 品牌
class BrandItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    logo = scrapy.Field()
    initial = scrapy.Field()
    date = scrapy.Field()
