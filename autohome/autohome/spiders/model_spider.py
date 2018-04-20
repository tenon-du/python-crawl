# coding=utf-8
import json
import time

import scrapy

from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.spiders import Rule

from autohome.items import ModelItem, levelMap


class ModelSpider(scrapy.Spider):
    name = "model"
    allowed_domains = 'autohome.com.cn'
    start_urls = ['https://www.autohome.com.cn/grade/carhtml/%s.html' % chr(ord('A') + i) for i in range(26)]

    # 测试地址
    # start_urls = ['https://www.autohome.com.cn/grade/carhtml/Q.html']

    rules = (
        # 字母分区页
        Rule(SgmlLinkExtractor(allow=(r'http://www.autohome.com.cn/grade/carhtml/\S.html',)), callback='parse', follow=True),

        # 车系详情
        Rule(SgmlLinkExtractor(allow=(r'.*www\.autohome\.com\.cn/\d+.*',)), callback='parse_model', follow=True),

        # 历史年款车型
        Rule(SgmlLinkExtractor(allow=(r'.*www\.autohome\.com\.cn/ashx/series_allspec\.ashx?s=\d+&y=\d+&l=\d+$',)),
             callback='parse_model_selled', follow=True),
    )

    def parse(self, response):
        print "===> " + response.url
        for serial_id in response.xpath('body/dl').re(r'id="s(\d+)"'):
            serial_page_url = "http://www.autohome.com.cn/" + serial_id
            request = scrapy.Request(url=serial_page_url, callback=self.parse_model, dont_filter=True)
            request.meta['serial_id'] = serial_id
            yield request

    def parse_model(self, response):
        print ("===> " + response.url)
        serial_id = response.meta['serial_id']

        # 判断此车系是否是在售车系
        stop_sell = response.xpath('/html/body').re(ur'(指导价（停售）)')
        if (not stop_sell) or len(stop_sell) == 0:

            # 解析在售车型
            panel = response.xpath('//div[@id="speclist20"]/*')
            size = len(panel)
            if size % 2 != 0:
                print('tag size[%d] is not expect, serial_id[%s].' % (size, serial_id))
                return
            for i in range(size / 2):
                group = panel[i * 2].xpath('div/span/text()')[0].extract()

                models = panel[i * 2 + 1]
                for model in models.xpath('li'):
                    item = ModelItem()
                    item['id'] = model.xpath('div[@class="interval01-list-cars"]/div/p/@data-gcjid')[0].extract()
                    item['sid'] = serial_id
                    item['name'] = model.xpath('div[@class="interval01-list-cars"]/div/p/a/text()')[0].extract()
                    item['classify'] = group
                    item['selling'] = '1'
                    item['date'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                    yield item

            # 解析车型类别
            try:
                level = response.xpath("//div[@class='path fn-clear']/div/a[2]/@href")[0].extract().strip('/')
                level = levelMap[level]
            except Exception as e:
                print('level not match, series_id[%s], msg[%s].' % (serial_id, e.message))
                return

            # 解析年限
            year_ids = response.xpath('//div[@id="drop2"]/div/ul/li/a/@data').extract()

            # 解析停售车型
            for year_id in year_ids:
                url = 'https://www.autohome.com.cn/ashx/series_allspec.ashx?s=%s&y=%s&l=%s' % (serial_id, year_id, level)
                request = scrapy.Request(url=url, callback=self.parse_model_selled, dont_filter=True)
                request.meta['serial_id'] = serial_id
                yield request
        else:
            # 停售车系
            models = response.xpath('//table/tboby/tr')
            if not models or len(models) == 0:
                models = response.xpath('//table/tr')

            for model in models:
                try:
                    item = ModelItem()
                    item['id'] = model.xpath('td[@class="name_d"]/div/a/@href')[0].re(r'spec/(\d+)/')[0]
                    item['sid'] = serial_id
                    item['name'] = model.xpath('td[@class="name_d"]/div/a/@title')[0].extract()
                    item['classify'] = item['name'][:6]
                    item['selling'] = '0'
                    item['date'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                    yield item
                except IndexError:
                    pass

    @staticmethod
    def parse_model_selled(response):
        print ("===> " + response.url)
        serial_id = response.meta['serial_id']
        data = json.loads(response.body_as_unicode())
        models = data['Spec']
        for model in models:
            item = ModelItem()
            item['id'] = model['Id']
            item['sid'] = serial_id
            item['name'] = model['Name']
            item['classify'] = model['GroupName']
            item['selling'] = '0'
            item['date'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            yield item
