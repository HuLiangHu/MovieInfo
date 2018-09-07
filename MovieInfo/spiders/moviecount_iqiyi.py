# -*- coding: utf-8 -*-
import scrapy
import json
import re
from scrapy.selector import Selector
from datetime import datetime

import requests
from lxml import etree

from MovieInfo.items import MoviecountsItem
from traceback import format_exc


def get_comingmoviename():
    doubanwill = 'https://movie.douban.com/coming'
    res = requests.get(doubanwill).text
    html = etree.HTML(res)
    name = html.xpath('//div[@class="grid-16-8 clearfix"]/div/table/tbody/tr/td/a/text()')
    return name


class IQiyiSpider(scrapy.Spider):
    name = "moviecount_iqiyi"
    moviename = get_comingmoviename()
    starturls = 'http://search.video.iqiyi.com/o?channel_name=%E7%94%B5%E5%BD%B1&if=html5&pageNum=1&pageSize=1&limit=20&category=&timeLength=0&releaseDate=&key={}&start=1&threeCategory=&u=b1m6wyyzos2knlxe698e1qqb&qyid=b1m6wyyzos2knlxe698e1qqb&pu=2125035081&video_allow_3rd=1&intent_result_number=10&intent_category_type=1&vfrm=2-3-0-1&_=1531981545941'
    #= 'http://mixer.video.iqiyi.com/jp/recommend/videos?albumId={}&channelId=10&cookieId=0ce767741c70369d933a80e5d0dd7131&withRefer=true&area=zebra&size=10&type=video&pru=&locale=&userId=&playPlatform=PC_QIYI&isSeriesDramaRcmd='
    dataapi='https://mixer.video.iqiyi.com/jp/recommend/videos?albumId={}&channelId=10&cookieId=e287ee06b869056d8becc26449a2679e&withRefer=true&area=zebra&size=10&type=video&pru=&locale=&userId=&playPlatform=PC_QIYI&isSeriesDramaRcmd='

    def start_requests(self):
        # self.server = connection.from_settings(self.settings)
        for name in self.moviename:
            url = self.starturls.format(name)
            yield scrapy.Request(url)

    def parse(self, response):
        result = json.loads(response.text)
        if result['data']['code'] == 0:

            if len(result['data']['docinfos']) > 0:
                albumn = result['data']['docinfos'][0]['albumDocInfo']
                if 'prevues' in albumn:
                    for item in albumn['prevues']:

                        # video = MoviecountsItem()
                        # video["title"] = item["itemTitle"]
                        # # video["view_count"]=i["playCount"]
                        # video["comefrom"] = "iqiyi"
                        # video["datetime"] = str(datetime.now())
                        # video["url"] = item["itemLink"]
                        # video["updatetime"] = str(datetime.today())

                        yield scrapy.Request('http://cache.video.qiyi.com/jp/pc/%s/' % item['tvId'],
                                             meta={"tvid":item['tvId']}, callback=self.parse_detail)

    # def parse_playcount(self, response):
    #     print(response.body_as_unicode())
    #     video = response.meta['video']
    #     video['view_count'] = re.search('{"\d+":(\d+)}', response.body_as_unicode()).group(1)
    #     yield video

    def parse_detail(self, response):
        #tvid = response.xpath('//div[@data-player-tvid]/@data-player-tvid').extract_first()
        tvid = response.meta['tvid']
        next_url = self.dataapi.format(tvid)
        yield scrapy.Request(next_url, callback=self.parse_grade)

    def parse_grade(self, response):
        data = re.findall(r'var tvInfoJs=(.*)', response.text)[0]
        jsondata = json.loads(data)
        for i in jsondata["mixinVideos"]:
            video = MoviecountsItem()
            video["title"] = i["name"]
            video["view_count"] = i["playCount"]
            video["comefrom"] = "iqiyi"
            video["datetime"] = str(datetime.now())
            video["url"] = i["url"]
            video["updatetime"]=str(datetime.today())
            yield video


    def error_back(self, e):
        """
        报错机制
        """
        self.logger.error(format_exc())













