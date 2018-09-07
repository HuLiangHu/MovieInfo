# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
import logging


from MovieInfo.items import DoubanTopItem, MovieNewsItem, MoviecountsItem


class MovieInfoMySqlPipeline(object):
    """A pipeline to store the item in a MySQL database.
    This implementation uses Twisted's asynchronous database API.
    """

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        '''init connection string'''
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            use_unicode=True,
            cp_reconnect=True)
        dbpool = adbapi.ConnectionPool('pymysql', **dbargs)
        return cls(dbpool)


    def process_item(self, item, spider):
        if isinstance(item, DoubanTopItem):
            d = self.dbpool.runInteraction(self._do_doubantop_upsert, item, spider)
        if isinstance(item, MovieNewsItem):
            if item['title'] != None:
                d = self.dbpool.runInteraction(self._do_movienews_upsert, item, spider)
        if isinstance(item, MoviecountsItem):
            if item['title'] != None:
                d = self.dbpool.runInteraction(self._do_movieplaycount_upsert, item, spider)


            # #d = self.dbpool.runInteraction(self._do_info_upsert, item, spider)
            # d.addErrback(self._handle_error, item, spider)
            # d.addBoth(lambda _: item)
            # return d

    def _do_doubantop_upsert(self, conn, item, spider):
        try:
            #print('正在写入doubantop数据到数据库')
            conn.execute("""replace into doubangrade (name,movieDate,doubanGrade,gradePeople,five,four,three,two
                            ,one)  values(%s,%s,%s,%s,%s,%s,%s,%s,%s);""",
                         (item['name'], item['movieDate'], item['doubanGrade'], item['gradePeople'],
                          item['five'], item['four'], item['three'], item['two'], item['one']))
        except Exception as e:
            logging.error(e)
        logging.info("Item insert in db: %r" % (item))

    def _do_movienews_upsert(self, conn, item, spider):
        try:
            #print('正在写入movienews数据到数据库')
            conn.execute("""replace into tbl_newsinfo (title,pubtime,content,website,newsurl,createdtime
                            )  values(%s,%s,%s,%s,%s,%s);""",
                         (item['title'], item['pubtime'], item['content'], item['comefrom'],
                          item['newsurl'], item['createdtime']))
        except Exception as e:
            logging.error(e)

        logging.info("Item insert in db: %r" % (item))

    def _do_movieplaycount_upsert(self, conn, item, spider):
        try:
            #print('正在写入movieplaycount数据到数据库')
            conn.execute("""replace into tbl_moviescounts (title,viewcount,website,createdtime,url
                            )  values(%s,%s,%s,%s,%s);""",
                         (item['title'], item['view_count'], item['comefrom'], item['datetime'], item["url"]
                          ))
        except Exception as e:
            logging.error(e)
        logging.info("Item insert in db: %r" % (item))
        # 异常处理

    def _handle_error(self, failue, item, spider):
        logging.error(failue)



