# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import mysql.connector

#DB info
dbhost = "192.168.1.106"
dbname = "kuaidaili"
dbuser = "root"
dbpass = "PEter)()3"

class KuaidailiPipeline(object):
    def process_item(self, item, spider):
        return item

class MySQLWritePipeline(object):
    def __init__(self):
        self.conn = mysql.connector.connect(user=dbuser,password=dbpass,database=dbname,host=dbhost,use_unicode=True)
        self.cursor = self.conn.cursor()
    def process_item(self, item, spider):
        try:
            sql="insert into proxy_server (id,ip,port,type,location,latency) values (null,%s,%s,%s,%s,%s)"
            self.cursor.execute(sql,(item['ip'].encode('utf-8'),item['port'].encode('utf-8'),item['type'].encode('utf-8'),item['location'].encode('utf-8'),item['latency'].encode('utf-8')))
            self.conn.commit()
        except :
            print "error"
        return item
