import scrapy

from youjia.items import PriceItem


class YouJiaSpider(scrapy.Spider):
    name = 'youjia'
    allowed_domains = 'www.bitauto.com'
    start_urls = ['http://www.bitauto.com/youjia/']

    def parse(self, response):
        for tr in response.xpath('//*[@class="oilTable"]/tbody/*'):
            item = PriceItem()
            item['area'] = tr.xpath('th[1]/a/text()')[0].extract()
            item['_89'] = tr.xpath('td[1]/text()')[0].extract()
            item['_92'] = tr.xpath('td[2]/text()')[0].extract()
            item['_95'] = tr.xpath('td[3]/text()')[0].extract()
            item['_0'] = tr.xpath('td[4]/text()')[0].extract()
            yield item

            try:
                item = PriceItem()
                item['area'] = tr.xpath('th[2]/a/text()')[0].extract()
                item['_89'] = tr.xpath('td[5]/text()')[0].extract()
                item['_92'] = tr.xpath('td[6]/text()')[0].extract()
                item['_95'] = tr.xpath('td[7]/text()')[0].extract()
                item['_0'] = tr.xpath('td[8]/text()')[0].extract()
                yield item
            except IndexError:
                pass
