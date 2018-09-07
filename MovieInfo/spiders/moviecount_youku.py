# -*- coding: utf-8 -*-
import scrapy
import re
from datetime import datetime
from lxml import etree
import requests
from MovieInfo.items import MoviecountsItem
from traceback import format_exc


class YoukuSpider(scrapy.Spider):
    def get_comingmoviename():
        doubanwill = 'https://movie.douban.com/coming'
        res = requests.get(doubanwill).text
        html = etree.HTML(res)
        name = html.xpath('//div[@class="grid-16-8 clearfix"]/div/table/tbody/tr/td/a/text()')
        return name
    # handle_httpstatus_list = [301]
    # # or
    # #handle_httpstatus_all = True
    name = "moviecount_youku"
    moviename=get_comingmoviename()
    starturls = 'http://so.youku.com/search_video/q_{}?spm=a2h0k.11417342.filter.dcategory&categories=96'

    def start_requests(self):
        for name in self.moviename:
        #name = '反贪风暴3'
            url = self.starturls.format(name)

            yield scrapy.Request(url,meta={'name':name},callback=self.parse,dont_filter=True)


    def parse(self, response):

        try:
            base_url = re.findall('http://v.youku.com(.*?)\\\\">', response.text)#正则匹配电影链接
            url = 'https://v.youku.com' + base_url[1]#构造新的链接
            yield scrapy.Request(url=url,callback=self.parse_grade,dont_filter=True)

        except IndexError:
            self.log(('没有找到电影:',response.meta['name'],'的官方预告片'))



    def parse_grade(self,response):
        contents = response.xpath('//*[@id="listitem_page1"]/div')
        for content in contents:
            item = MoviecountsItem()
            item['title'] = content.xpath('a/div[@class="title"]/text()').extract_first()
            #item['duration'] = content.xpath('a/div/span[@class="c-time"]/span/text()').extract_first()
            item["comefrom"] = "youku"
            item["datetime"] = str(datetime.now())

            item['view_count'] = content.xpath('a/div[@class="status"]/span/text()').re('(.*?)次播放')[0]

            item['view_count'] = content.xpath('a/div[@class="status"]/span/text()').re('(.*)次播放')[0]
            # if u'万' in item['view_count']:
            #     item['view_count'] = int(float(item['view_count'].replace(u'万',''))*10000)
            # elif u'亿' in item['view_count']:
            #     item['view_count'] = int(float(item['view_count'].replace(u'亿', '') )* 100000000)

            link = content.xpath('a/@href').extract_first()
            item['url'] ='http:'+link
            item["updatetime"] = str(datetime.today())

            yield item

    def error_back(self, e):
        """
        报错机制
        """
        self.logger.error(format_exc())
