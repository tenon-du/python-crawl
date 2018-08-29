# coding=utf-8

import scrapy
from xpinyin import Pinyin

from region.items import RegionItem


class RegionSpider(scrapy.Spider):
    name = "region"

    def start_requests(self):
        url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2017/index.html'
        yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    # 解析省份
    def parse(self, response):
        print '==> %s' % response.url
        p = Pinyin()
        try:
            for tr in response.xpath('//tr[@class="provincetr"]'):
                for td in tr.xpath('td'):
                    item = RegionItem()
                    item['adCode'] = td.xpath('a/@href')[0].extract()[0:-5]
                    item['name'] = td.xpath('a/text()')[0].extract()
                    item['py'] = p.get_pinyin(item['name'], ' ')
                    item['initial'] = p.get_initials(item['name'], '')[0:1]
                    item['level'] = 1
                    item['parent'] = ''
                    yield item

                    url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2017/%s.html' % item['adCode']
                    request = scrapy.Request(url, callback=self.parse_city, dont_filter=True)
                    request.meta['pid'] = item['adCode']
                    yield request
        except IndexError:
            pass

    # 解析城市
    def parse_city(self, response):
        print '==> %s' % response.url
        pid = response.meta['pid']

        p = Pinyin()

        for tr in response.xpath('//tr[@class="citytr"]'):
            item = RegionItem()
            item['adCode'] = tr.xpath('td[1]/a/text()')[0].extract()[0:4]
            item['name'] = tr.xpath('td[2]/a/text()')[0].extract()
            item['py'] = p.get_pinyin(item['name'], ' ')
            item['initial'] = p.get_initials(item['name'], '')[0:1]
            item['level'] = 2
            item['parent'] = pid
            yield item

            url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2017/%s/%s.html' % (pid, item['adCode'])
            request = scrapy.Request(url, callback=self.parse_county, dont_filter=True)
            request.meta['pid'] = item['adCode']
            yield request

    # 解析区(县)
    def parse_county(self, response):
        print '==> %s' % response.url
        pid = response.meta['pid']

        p = Pinyin()
        for tr in response.xpath('//tr[@class="countytr"]'):
            item = RegionItem()
            item['level'] = 3
            item['parent'] = pid

            try:
                item['adCode'] = tr.xpath('td[1]/a/text()')[0].extract()[0:6]
                item['name'] = tr.xpath('td[2]/a/text()')[0].extract()

                url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2017/%s/%s/%s.html' % (pid[0:2], pid[2:4], item['adCode'])
                request = scrapy.Request(url, callback=self.parse_town, dont_filter=True)
                request.meta['pid'] = item['adCode']
                yield request
            except IndexError:
                item['adCode'] = tr.xpath('td[1]/text()')[0].extract()[0:6]
                item['name'] = tr.xpath('td[2]/text()')[0].extract()

            item['py'] = p.get_pinyin(item['name'], ' ')
            item['initial'] = p.get_initials(item['name'], '')[0:1]
            yield item

    # 解析街道(乡镇)
    def parse_town(self, response):
        print '==> %s' % response.url
        pid = response.meta['pid']

        p = Pinyin()

        for tr in response.xpath('//tr[@class="towntr"]'):
            item = RegionItem()
            item['adCode'] = tr.xpath('td[1]/a/text()')[0].extract()[0:9]
            item['name'] = tr.xpath('td[2]/a/text()')[0].extract()
            item['py'] = p.get_pinyin(item['name'], ' ')
            item['initial'] = p.get_initials(item['name'], '')[0:1]
            item['level'] = 4
            item['parent'] = pid
            yield item

            url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2017/%s/%s/%s/%s.html' % (
                pid[0:2], pid[2:4], pid[4:6], item['adCode'])
            request = scrapy.Request(url, callback=self.parse_village, dont_filter=True)
            request.meta['pid'] = item['adCode']
            yield request

    # 解析居委会(村)
    @staticmethod
    def parse_village(response):
        print '==> %s' % response.url
        pid = response.meta['pid']

        p = Pinyin()
        try:
            for tr in response.xpath('//tr[@class="villagetr"]'):
                item = RegionItem()
                item['adCode'] = tr.xpath('td[1]/text()')[0].extract()
                item['name'] = tr.xpath('td[3]/text()')[0].extract()
                item['py'] = p.get_pinyin(item['name'], ' ')
                item['initial'] = p.get_initials(item['name'], '')[0:1]
                item['level'] = 5
                item['parent'] = pid
                yield item
        except IndexError:
            pass
