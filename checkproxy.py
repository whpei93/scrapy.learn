#!/usr/bin/python
# coding:utf-8

import mysql.connector
import requests

#DB info
dbhost = "192.168.1.106"
dbname = "kuaidaili"
dbuser = "root"
dbpass = "PEter)()3"

ClearSQL='delete from proxy_server where id not in (select * from (select max(id) from proxy_server group by ip,port) as b)'
conn = mysql.connector.connect(user=dbuser, password=dbpass, database=dbname, host=dbhost, use_unicode=True)
cursor = conn.cursor()
cursor.execute(ClearSQL)
cursor.commit()

cursor.execute('select type,ip,port from proxy_server')
url1 = 'http://www.baidu.com'
url2 = 'http://www.google.com'
type = 'http'
ip =

proxies = type+'://'+ip+':'+port
r=requests.get(url)
