# coding=utf-8

import scrapy

from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.spiders import Rule


class ModelSpider(scrapy.Spider):
    name = "model"
    allowed_domains = 'autohome.com.cn'
    # start_urls = ['https://www.autohome.com.cn/grade/carhtml/%s.html' % chr(ord('A') + i) for i in range(26)]

    # 测试地址
    start_urls = ['https://www.autohome.com.cn/grade/carhtml/A.html']

    rules = (
        # 字母分区页
        Rule(SgmlLinkExtractor(allow=(r'http://www.autohome.com.cn/grade/carhtml/\S.html',)), callback='parse',
             follow=True),
    )

    def parse(self, response):
        print("===>", response.url)
        # for brands in response.xpath('body/dl'):
        #     serials = brands.xpath('dd/ul/li')
        #     for serial in serials:
        #         try:
        #             item = SeriesItem()
        #             item['bid'] = brands.xpath('@id')[0].extract()
        #             item['vendor'] = brands.xpath('dd/div/text()')[0].extract()
        #             item['id'] = serial.xpath('@id')[0].extract()[1:]
        #             item['name'] = serial.xpath('h4/a/text()')[0].extract()
        #             item['date'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        #
        #             yield item
        #         except IndexError:
        #             pass
