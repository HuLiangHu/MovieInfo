# -*- coding: utf-8 -*-
import scrapy
from scrapy.crawler import CrawlerProcess
from MovieInfo.spiders.moviecount_iqiyi import IQiyiSpider
from MovieInfo.spiders.movienews_sohu import SouhuNewsSpider
from MovieInfo.spiders.moviecount_tencent import QQSpider
from MovieInfo.spiders.moviecount_youku import YoukuSpider
from MovieInfo.spiders.movienews_fenghuang import FenghuangSpider
from MovieInfo.spiders.movienews_shiguang import ShiguangSpider
from MovieInfo.spiders.movienews_sina import XinglangSpider
from MovieInfo.spiders.movienews_wangyi import WangyiSpider
from MovieInfo.spiders.movienews_tencent import TengxunSpider

from scrapy.utils.project import get_project_settings
process = CrawlerProcess(get_project_settings())
process.crawl(IQiyiSpider)
process.crawl(QQSpider)
process.crawl(YoukuSpider)
process.crawl(FenghuangSpider)
process.crawl(ShiguangSpider)
process.crawl(XinglangSpider)
process.crawl(SouhuNewsSpider)
process.crawl(WangyiSpider)
process.crawl(TengxunSpider)

process.start()