# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.selector import Selector

from datetime import datetime


# from scrapy_redis import connection
from MovieInfo.items import MovieNewsItem


class ShiguangSpider(scrapy.Spider):


    name = "movienews_shiguang"

    start_urls = ['http://news.mtime.com/']

    def start_requests(self):
        # self.server = connection.from_settings(self.settings)

        for url in self.start_urls:
            yield scrapy.Request(url)

    def parse(self, response):
        data = response.xpath('//h4/a/@href').extract()
        for url in data:
            yield scrapy.Request(url,callback=self.parse_grade)


    def parse_grade(self,response):
        if response.status==200:
            selector = Selector(response)
            item = MovieNewsItem()
            item["title"]=selector.xpath('//h2/text()').extract_first()
            item["createdtime"]=str(datetime.now())
            try:
                item["pubtime"]=selector.xpath('//p[@class="mt15 ml25 newstime "]/text()').extract_first().strip()
            except:
                item['pubtime'] =selector.xpath('//p[@class="mt15 ml25 newstime "]/text()').extract_first()
            item["comefrom"]="时光新闻"
            item["newsurl"] = response.url
            contenttext=selector.xpath('//div[@id="newsContent"]/div/text()').extract()
            if contenttext==[]:
                contenttext=selector.xpath('//div[@id="newsContent"]/p/text()').extract()
            content= contenttext
            item["content"] = "".join(content).strip()
            return item

    def error_back(self, e):
        """
        报错机制
        """
        self.logger.error(format_exc())


