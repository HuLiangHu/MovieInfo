# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector

from datetime import datetime


# from scrapy_redis import connection
from MovieInfo.items import MovieNewsItem


class TengxunSpider(scrapy.Spider):

    name = "movienews_tencent"
    start_urls = ['http://ent.qq.com/movie/']

    def start_requests(self):
        # self.server = connection.from_settings(self.settings)

        for url in self.start_urls:
            yield scrapy.Request(url)

    def parse(self, response):
        detail_urls = response.xpath('//div[@class="Q-tpList"]/div/a/@href').extract()
        for url in detail_urls:
            #print(url)
            yield scrapy.Request(url,callback=self.parse_grade,dont_filter=True)


    def parse_grade(self,response):
        if response.status==200:
            selector = Selector(response)
            item = MovieNewsItem()
            item["title"]=selector.xpath('//div[@class="LEFT"]/h1/text()').extract_first()
            item["createdtime"]=str(datetime.now())
            item["pubtime"]=selector.xpath('//meta[@name="_pubtime"]/@content').extract_first()
            item["comefrom"]="腾讯新闻"
            item["newsurl"] = response.url
            content= selector.xpath('//div[@class="content-article"]/p/text()').extract()
            item["content"] = "".join(content).strip()

            return item

