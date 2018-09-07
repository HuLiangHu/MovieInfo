# -*- coding: utf-8 -*-

import scrapy
import json
import re
from scrapy.selector import Selector
from datetime import datetime

import requests
from lxml import etree

from MovieInfo.items import MoviecountsItem


def get_comingmoviename():
    doubanwill = 'https://movie.douban.com/coming'
    res = requests.get(doubanwill).text
    html = etree.HTML(res)
    name = html.xpath('//div[@class="grid-16-8 clearfix"]/div/table/tbody/tr/td/a/text()')
    return name


class LetvSpider(scrapy.Spider):

    name = "moviecount_letv"
    moviename=get_comingmoviename()
    testurl=['http://www.le.com/ptv/vplay/31365978.html']
    starturls = 'http://search.lekan.letv.com/lekan/apisearch_json.so?from=pc&jf=1&hl=1&dt=1,2&ph=420001,420002&show=4&pn=1&ps=35&wd={}&lc=b036c8cfc33a1c3f4750ee96da06fb4a&uid=&session=&_=1518061526767'
    queryurl='https://count.vrs.sohu.com/count/query.action?videoId={}'
    dataapi='https://pl.hd.sohu.com/videolist?playlistid={}&o_playlistId=&pianhua=1&pageRule=1&pagesize=999&order=1&cnt=1&ssl=0&preVideoRule=1'
    def start_requests(self):
        # self.server = connection.from_settings(self.settings)
        for name in self.moviename:
            url = self.starturls.format(name)
            yield scrapy.Request(url)


    def parse(self, response):

        data = json.loads(response.text)
        videourl = 'http://www.le.com/ptv/vplay/{}.html'
        for i in data["data_list"]:
            item = MoviecountsItem()
            item["title"]=i["highLightName"]
            item["view_count"]=i["playCount"]
            item["comefrom"] = "letv"
            item["datetime"] = str(datetime.now())
            item["url"] = videourl.format(i["vid"])
            item["updatetime"] = str(datetime.today())
            yield item



















