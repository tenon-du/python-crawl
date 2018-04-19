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


# 车系
class SerialItem(scrapy.Item):
    id = scrapy.Field()
    bid = scrapy.Field()
    name = scrapy.Field()
    vendor = scrapy.Field()
    date = scrapy.Field()


# 车型
class ModelItem(scrapy.Item):
    id = scrapy.Field()
    sid = scrapy.Field()
    name = scrapy.Field()
    pic = scrapy.Field()
    group = scrapy.Field()
    status = scrapy.Field()
    date = scrapy.Field()


# 车型类别key和车型类别ID的对应关系
levelMap = {
    'a00': 1,
    'a0': 2,
    'a': 3,
    'b': 4,
    'c': 5,
    'd': 6,
    'suv': 7,
    'mpv': 8,
    's': 9,
    'p': 10,
    'mb': 11,
    'suva0': 16,
    'suva': 17,
    'suvb': 18,
    'suvc': 19,
    'suvd': 20
}
