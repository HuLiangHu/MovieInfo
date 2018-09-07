# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import scrapy
import json
import re
from scrapy.selector import Selector




# from scrapy_redis import connection


from MovieInfo.items import DoubanTopItem


class DoubanMoviesSpider(scrapy.Spider):

    name = "doubantop"
    start_urls = ['https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=电影,香港&start=0',
                  'https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=电影,大陆&start=0']

    apikeys = ['088acf79cc38fde819a06e6d64aaf9b8',
               '01e1232b205f406405a36981611dc12c', '03405aad00de230c09c11007029a6924']

    def start_requests(self):
        # self.server = connection.from_settings(self.settings)

        for url in self.start_urls:
            yield scrapy.Request(url)

    def parse(self, response):
        subjects = json.loads(response.body_as_unicode())
        if len(subjects['data']) > 0:
            start = int(re.search('start=(\d+)', response.url).group(1))
            nextPage = re.sub('start=\d+', 'start=%s' % (start + 20), response.url)
            yield scrapy.Request(nextPage)
        for subject in subjects['data']:
            url = subject["url"]
            id = subject["id"]
            yield scrapy.Request(url,callback=self.parse_grade)


    def parse_grade(self,response):
        selector = Selector(response)
        item = DoubanTopItem()
        item["name"]=selector.xpath('//span[@property="v:itemreviewed"]/text()').extract_first()
        item["movieDate"]=selector.xpath('//span[@property="v:initialReleaseDate"]/text()').extract_first()
        item["doubanGrade"]=selector.xpath('//strong[@property]/text()').extract_first()
        item["gradePeople"]=selector.xpath('//span[@property="v:votes"]/text()').extract_first()
        rating = selector.xpath('//span[@class="rating_per"]/text()').extract()
        item["five"]=rating[0]
        item["four"]=rating[1]
        item["three"]=rating[2]
        item["two"]=rating[3]
        item["one"]=rating[4]
        return item

