# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.selector import Selector

from datetime import datetime


# from scrapy_redis import connection
from MovieInfo.items import MovieNewsItem


class WangyiSpider(scrapy.Spider):


    name = "movienews_wangyi"
    start_urls = [
                    'http://ent.163.com/special/000381Q1/newsdata_movieidx.js?callback=data_callback',
                    'http://ent.163.com/special/000381Q1/newsdata_movieidx_02.js?callback=data_callback',
                    'http://ent.163.com/special/000381Q1/newsdata_movieidx_03.js?callback=data_callback']

    def start_requests(self):
        # self.server = connection.from_settings(self.settings)

        for url in self.start_urls:
            yield scrapy.Request(url)

    def parse(self, response):

        data = json.loads(response.body_as_unicode()[14:-1])
        for url in data:
            yield scrapy.Request(url["docurl"],callback=self.parse_grade)


    def parse_grade(self,response):
        if response.status==200:
            selector = Selector(response)
            item = MovieNewsItem()
            item["title"]=selector.xpath('//div[@class="post_content_main"]/h1/text()').extract_first()
            item["createdtime"]=str(datetime.now())
            item["pubtime"]=selector.xpath('//meta[@property="article:published_time"]/@content').extract_first()
            item["comefrom"]="网易新闻"
            item["newsurl"] = response.url
            contenttext=selector.xpath('//div[@class="post_text"]/p/text()').extract()
            if contenttext==[]:
                contenttext = selector.xpath('//div[@class="end-text"]/p/text()').extract()
            if len(contenttext)<3:
                contenttext=selector.xpath('//div[@class="end-text"]/p/span/text()').extract()

            content= contenttext
            item["content"] = "".join(content).strip()

            return item

    def error_back(self, e):
        """
        报错机制
        """
        self.logger.error(format_exc())


