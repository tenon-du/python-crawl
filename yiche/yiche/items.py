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


# 车系
class SerialItem(scrapy.Item):
    id = scrapy.Field()
    bid = scrapy.Field()
    name = scrapy.Field()
    vendor = scrapy.Field()
    logo = scrapy.Field()
    sell = scrapy.Field()


# 车型
class ModelItem(scrapy.Item):
    id = scrapy.Field()
    sid = scrapy.Field()
    name = scrapy.Field()
    classify = scrapy.Field()
    sell = scrapy.Field()
