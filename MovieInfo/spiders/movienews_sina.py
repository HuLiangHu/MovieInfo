# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.selector import Selector

from datetime import datetime


# from scrapy_redis import connection
from MovieInfo.items import MovieNewsItem


class XinglangSpider(scrapy.Spider):


    name = "movienews_sina"

    start_urls = ['http://feed.mix.sina.com.cn/api/roll/get?pageid=51&lid=740&num=50&versionNumber=1.2.8&page=1',
                  'http://feed.mix.sina.com.cn/api/roll/get?pageid=51&lid=740&num=50&versionNumber=1.2.8&page=2']
    custom_settings = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'genTime=1531151398; ustat=__223.166.231.123_1531151398_0.19305900; vt=4; Apache=1301129587489.4512.1535197669740; SINAGLOBAL=1301129587489.4512.1535197669740; ULV=1535197669741:1:1:1:1301129587489.4512.1535197669740:; historyRecord={"href":"https://ent.sina.cn/film/chinese/2018-08-24/detail-ihicsiaw1011271.d.html","refer":""}',
        'Host': 'ent.sina.cn',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }
    def start_requests(self):
        # self.server = connection.from_settings(self.settings)

        for url in self.start_urls:
            yield scrapy.Request(url)

    def parse(self, response):
        data =json.loads(response.text)
        for url in data['result']['data']:
            new_url = url["wapurl"]
            yield scrapy.Request(new_url,callback=self.parse_grade)


    def parse_grade(self,response):
        if response.status==200:
            selector = Selector(response)
            item = MovieNewsItem()
            item["title"]=selector.xpath('//h1/text()').extract_first()
            item["createdtime"]=str(datetime.now())
            item["pubtime"]=selector.xpath('//meta[@property="article:published_time"]/@content').extract_first()
            if item["pubtime"]==None:
                item["pubtime"]=selector.xpath('//span[@id="pub_date"]/text()').extract_first()
            item["comefrom"]="新浪新闻"
            item["newsurl"] = response.url
            contenttext=selector.xpath('//div[@class="article"]/p/text()').extract()
            content= contenttext
            item["content"] = "".join(content).strip()
            return item

    def error_back(self, e):
        """
        报错机制
        """
        self.logger.error(format_exc())


