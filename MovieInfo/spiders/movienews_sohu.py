# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.selector import Selector
from MovieInfo.items import MovieNewsItem
from datetime import datetime


# from scrapy_redis import connection


class SouhuNewsSpider(scrapy.Spider):

    name = "movienews_souhu"
    start_urls = ['http://yule.sohu.com/movie.shtml']

    def start_requests(self):
        # self.server = connection.from_settings(self.settings)

        for url in self.start_urls:
            yield scrapy.Request(url)

    def parse(self, response):
        data = response.xpath('//div[@class="f14list"]/ul/li/a/@href').extract()
        for url in data:
            yield scrapy.Request(url,callback=self.parse_grade)


    def parse_grade(self,response):
        if response.status==200:
            selector = Selector(response)
            item = MovieNewsItem()
            item["title"]=selector.xpath('//h1/text()').extract_first()
            item["createdtime"]=str(datetime.now())
            item["pubtime"]=selector.xpath('//meta[@property="og:release_date"]/@content').extract_first()
            item["comefrom"]="搜狐新闻"
            item["newsurl"] = response.url
            contenttext=selector.xpath('//article/p/text()').extract()
            content= contenttext
            item["content"] = "".join(content).strip()
            return item

    def error_back(self, e):
        """
        报错机制
        """
        self.logger.error(format_exc())


