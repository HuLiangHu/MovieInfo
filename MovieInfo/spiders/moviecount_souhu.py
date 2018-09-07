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

class SouhuSpider(scrapy.Spider):

    name = "moviecount_souhu"
    moviename=get_comingmoviename()
    starturls = 'https://so.tv.sohu.com/mts?box=1&wd={}'
    queryurl='https://count.vrs.sohu.com/count/query.action?videoId={}'
    dataapi='https://pl.hd.sohu.com/videolist?playlistid={}&o_playlistId=&pianhua=1&pageRule=1&pagesize=999&order=1&cnt=1&ssl=0&preVideoRule=1'
    def start_requests(self):
        # self.server = connection.from_settings(self.settings)
        for name in self.moviename:
            url = self.starturls.format(name)
            yield scrapy.Request(url)


    def parse(self, response):
        ids = response.xpath('//p[@class="lt-info"]/a/@_s_a').extract()
        for sid in ids:
            if sid !='0':
                next_url = self.dataapi.format(sid)
                yield scrapy.Request(next_url,callback=self.parse_grade)
                return

    def parse_grade(self,response):
        jsondata = json.loads(response.text)
        datadict={}
        urldict={}
        vid=[]
        for dt in jsondata['prevideos']:
            vid.append(str(dt["vid"]))
            datadict[dt["vid"]]=dt["showName"]
            urldict[dt["vid"]]=dt["pageUrl"]
        for dt1 in jsondata['videos']:
            vid.append(str(dt1["vid"]))
            datadict[dt1["vid"]]=dt1["showName"]
            urldict[dt1["vid"]]=dt1["pageUrl"]


        idgroup=",".join(vid)
        res = requests.get(self.queryurl.format(idgroup)).text
        countjson = re.findall(r'count=(.*?);',res)[0]
        countdata = json.loads(countjson)
        for video in countdata["videos"]:
            if int(video["videoId"]) in datadict.keys():
                item = MoviecountsItem()
                item["title"]=datadict[int(video["videoId"])]
                item["view_count"]=video["count"]
                item["comefrom"]="souhu"
                item["datetime"]=str(datetime.now())
                item["url"]="http:"+urldict[int(video["videoId"])]
                item["updatetime"]=str(datetime.today())
                yield item















