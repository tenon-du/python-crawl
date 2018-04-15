import scrapy


class toutiao(scrapy.Spider):
    name = "toutiao"
    start_urls = ["https://www.toutiao.com/ch/news_car/"]

    def parse(self, response):
        print(response)

        title = response.xpath( "/html/body/div/div[4]/div[2]/div[2]/div/div/div/ul/li[1]/div/div[1]/div/div[1]/a/text()").extract()
        icon = response.xpath("/html/body/div/div[4]/div[2]/div[2]/div/div/div/ul/li[1]/div/div[2]/a/img/@src").extract()

        for i, j in zip(title, icon):
            print(i, ":", j)
