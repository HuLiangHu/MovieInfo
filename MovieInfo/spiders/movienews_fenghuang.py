# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.selector import Selector
from datetime import datetime


# from scrapy_redis import connection
from MovieInfo.items import MovieNewsItem


class FenghuangSpider(scrapy.Spider):

    name = "movienews_fenghuang"
    start_urls = ['http://ent.ifeng.com/listpage/6/1/list.shtml',
                  'http://ent.ifeng.com/listpage/6/2/list.shtml',
                  'http://ent.ifeng.com/listpage/6/3/list.shtml',
                  'http://ent.ifeng.com/listpage/6/4/list.shtml']

    def start_requests(self):
        # self.server = connection.from_settings(self.settings)

        for url in self.start_urls:
            yield scrapy.Request(url)

    def parse(self, response):
        data = response.xpath('//h2/a/@href').extract()
        for url in data:
            yield scrapy.Request(url,callback=self.parse_grade)


    def parse_grade(self,response):
        if response.status==200:
            selector = Selector(response)
            item = MovieNewsItem()
            item["title"]=selector.xpath('//div[@id="artical"]/h1/text()').extract_first()
            item["createdtime"]=str(datetime.now())
            item["pubtime"]=selector.xpath('//meta[@name="og:time"]/@content').extract_first()
            item["comefrom"]="凤凰新闻"
            item["newsurl"] = response.url
            contenttext=selector.xpath('//div[@id="main_content"]/p/text()').extract()
            content= contenttext
            item["content"] = "".join(content).strip()
            return item

    def error_back(self, e):
        """
        报错机制
        """
        self.logger.error(format_exc())


