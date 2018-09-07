# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# class MovieinfoItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass

class DoubanTopItem(scrapy.Item):
    name = scrapy.Field()
    movieDate = scrapy.Field(default=None)
    doubanGrade = scrapy.Field(default=0)
    gradePeople = scrapy.Field(default=0)
    five = scrapy.Field(default=0)
    four = scrapy.Field(default=0)
    three = scrapy.Field(default=0)
    two = scrapy.Field(default=0)
    one = scrapy.Field(default=0)

class MovieNewsItem(scrapy.Item):
    title = scrapy.Field()
    pubtime=scrapy.Field()
    createdtime=scrapy.Field()
    comefrom=scrapy.Field()
    content=scrapy.Field(default=None)
    newsurl=scrapy.Field()

class MoviecountsItem(scrapy.Item):
    title=scrapy.Field()
    view_count=scrapy.Field()
    comefrom=scrapy.Field()
    datetime=scrapy.Field()
    url=scrapy.Field()
    updatetime=scrapy.Field()






