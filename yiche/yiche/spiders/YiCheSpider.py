# coding=utf-8

import scrapy


class YiCheSpider(scrapy.Spider):
    name = "yiche"
    allowed_domains = 'car.bitauto.com/tree_chexing/'
    start_urls = ['http://car.bitauto.com/tree_chexing/mb_9/']

    def parse(self, response):
        print('===> start')
        for letter in response.xpath('//*[@id="treeList"]/ul/li'):
            print(letter.xpath('div/text()'))
            pass
