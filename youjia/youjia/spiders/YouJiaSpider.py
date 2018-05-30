import scrapy

from youjia.items import PriceItem


class YouJiaSpider(scrapy.Spider):
    name = 'youjia'
    allowed_domains = 'youjia.chemcp.com'
    start_urls = ['http://youjia.chemcp.com/']

    def parse(self, response):
        for tr in response.xpath('//*[@class="chem_3"]/div[1]/div[2]/table/*'):
            try:
                item = PriceItem()
                item['area'] = tr.xpath('td[1]/a/text()')[0].extract()
                item['_89'] = tr.xpath('td[2]/text()')[0].extract()
                item['_92'] = tr.xpath('td[3]/text()')[0].extract()
                item['_95'] = tr.xpath('td[4]/text()')[0].extract()
                item['_0'] = tr.xpath('td[5]/text()')[0].extract()
                item['update_time'] = tr.xpath('td[6]/text()')[0].extract()
                yield item
            except IndexError:
                pass

