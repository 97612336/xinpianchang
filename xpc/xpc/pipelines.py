# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class XpcPipeline(object):

    def __init__(self):
        self.conn=None
        self.cur=None

    def open_spider(self,spider):
        self.conn=pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='root123456',
            db='xpc',
            charset='utf8'
        )
        self.cur=self.conn.cursor()

    def process_item(self, item, spider):
        cols = item.keys()
        values = [item[col] for col in cols]
        cols = ['`%s`' % key for key in cols]
        sql = "INSERT INTO `"+item.table_name+"`(" + ','.join(cols) + ") VALUES (" + ','.join(['%s'] * len(cols)) + ");"
        self.cur.execute(sql, values)
        self.conn.commit()
        return item

    def close_spider(self,spider):
        self.cur.close()
        self.conn.close()
