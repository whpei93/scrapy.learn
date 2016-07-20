# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb

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
        self.conn = MySQLdb.connect(user=dbuser,passwd=dbpass,db=dbname,host=dbhost)
        self.cursor = self.conn.cursor()
    def process_item(self, item, spider):
        try:
            #self.cursor.execute("insert into proxy_server (id,ip,port,type,location,latency) values (%s,%s,%s,%s,%s,%s)",[None,item['ip'].encode('utf-8'),item['port'].encode('utf-8'),item['type'].encode('utf-8'),item['location'].encode('utf-8'),item['latency'].encode('utf-8')])
            #self.conn.commit()
            print item
        except MySQLdb.Error,e:
            print "Error %d :%s" %(e.args[0],e.args[1])
        return item
