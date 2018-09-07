# -*- coding: utf-8 -*-
import scrapy
import json
import re
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

class QQSpider(scrapy.Spider):

    name = "moviecount_tencent"
    moviename=get_comingmoviename()
    starturls = 'http://v.qq.com/x/search/?q={}&stag=4&filter=sort%3D0%26pubfilter%3D0%26duration%3D0%26tabid%3D1%26resolution%3D0#!filtering=1'
    #starturls = 'http://node.video.qq.com/x/api/msearch?contextValue=last_end%3D15%26response%3D1&filterValue=tabid%3D1&searchSession=qid%3DadbB4yuiwVs7ShfizCnlHOfA3FR_rLwBUtFkWwqzmpFB72GejvgG-A&keyWord={}&contextType=3'
    dataapi = 'https://union.video.qq.com/fcgi-bin/data?otype=json&tid=682&appid=20001238&appkey=6c03bbe9658448a4&idlist={}&callback=jQuery19103901585250857962_1517797975248&_=1517797975249'
    def start_requests(self):
        # self.server = connection.from_settings(self.settings)
        for name in self.moviename:
            url = self.starturls.format(name)
            yield scrapy.Request(url)


    def parse(self, response):
        url = response.xpath('//h2[@class="result_title"]/a/@href').extract_first()
        url =url.replace('http','https')#解决302重定向问题
        yield scrapy.Request(url,callback=self.parse_next)
        '''
        result = json.loads(response.text)
        if result['errCode'] == 0:
            if len(result['uiData'])>0:
                item = result['uiData'][0]
                yield item['data'][0]
                #url = response.xpath('//h2[@class="result_title"]/a/@href').extract_first()
                #yield scrapy.Request(url,callback=self.parse_next)
        '''
    def parse_next(self, response):
        ids = response.xpath('//div[@class="scroll_wrap"]/div[@style]/div/ul/li/@id').extract()
        iddict = []
        tenidlist=[]
        for mid in ids:
            iddict.append(mid)
        count = len(iddict)
        for i in range(0,count):
            if (i+1) % 30 == 0:
                tenidlist.append(iddict[i])
                tenid = ",".join(tenidlist)
                next_url = self.dataapi.format(tenid)
                yield scrapy.Request(next_url, callback=self.parse_grade)
                tenidlist.clear()
            if i ==count-1:
                tenid = ",".join(tenidlist)
                next_url = self.dataapi.format(tenid)
                yield scrapy.Request(next_url, callback=self.parse_grade)
                tenidlist.clear()
            else:
                tenidlist.append(iddict[i])

    def parse_grade(self,response):
        data = re.findall(r"\(({.*?})\)",response.text)[0]
        jsondata = json.loads(data)
        movieurl='https://v.qq.com/x/cover/5y95zy4idzqf6hc/{}.html'
        try:
            for dt in jsondata['results']:
                item = MoviecountsItem()
                item["title"]=dt["fields"]['vname_title']
                item["view_count"]=dt["fields"]["view_all_count"]
                item["comefrom"]="tengxun"
                item["url"]=movieurl.format(dt["fields"]["vid"])
                item["datetime"]=str(datetime.now())
                #item["updatetime"]=str(datetime.today())
                yield item
        except:
            pass

    def error_back(self, e):
        """
        报错机制
        """
        self.logger.error(format_exc())












