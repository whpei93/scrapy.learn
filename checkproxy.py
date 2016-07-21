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
conn = mysql.connector.connect(user=dbuser, password=dbpass, database=dbname, use_unicode=True)
cursor = conn.cursor()
cursor.execute(ClearSQL)
conn.commit()
cursor.execute('select type,ip,port,location from proxy_server')
proxies = cursor.fetchall()

url_list=['http://www.baidu.com','http://www.google.com']

def check_proxy(server,*urllist):
    type = str(server[0]).lower()
    ip = str(server[1])
    port = str(server[2])
    location = location = server[3].encode('utf-8')
    conn2 = mysql.connector.connect(user=dbuser, password=dbpass, database='valid_proxies', use_unicode=True)
    cursor2 = conn2.cursor()
    count = 0 
    if len(type.split(',')) == 1:
        proxy={}
        proxy[type] = type+'://'+ip+':'+port
        for url in urllist:
            try:
                res = requests.get(url,proxies=proxy,timeout=10)
                if res.status_code != 200:
                    print "proxy : %s unable to use" %proxy[type]
                    #cursor.execute('delete from proxy_server where ip=%s and port=%s',(ip,port))
                    #conn.commit()
                    count += 1
                else:
                    latency = res.elapsed.microseconds/1000
                    testurl = url.split('/')[-1]
                    print "proxy : %s able to use, latency : %d ms" %(proxy[type],latency)
                    cursor2.execute('insert into valid_server (id,ip,port,type,latency,location,testurl) values(null,%s,%s,%s,%s,%s,%s)',(ip,port,type,latency,location,testurl))
                    conn2.commit()
            except requests.exceptions.RequestException,e:
                print e,"proxy : %s unable to use" %proxy[type]
                cursor.execute('delete from proxy_server where ip=%s and port=%s',(ip,port))
                conn.commit()
                count += 1
        if count == len(urllist):
            print "faield to test"
            cursor.execute('delete from proxy_server where ip=%s and port=%s',(ip,port))
            conn.commit()
        else:
            pass
    else:
        for url in urllist:
            for t in type.split(','):
                proxy={}
                proxy[t.strip()] = t.strip()+'://'+ip+':'+port
                try:
                    res = requests.get(url,proxies=proxy,timeout=10)
                    if res.status_code != 200:
                        print "proxy : %s unable to use" %proxy[t.strip()]
                        cursor.execute('delete from proxy_server where ip=%s and port=%s',(ip,port))
                        conn.commit()
                        count += 1
                    else:
                        latency = res.elapsed.microseconds/1000
                        testurl = url.split('/')[-1]
                        cursor2.execute('insert into valid_server (id,ip,port,type,latency,location,testurl) values(null,%s,%s,%s,%s,%s,%s)',(ip,port,t.strip(),latency,location,testurl))
                        print "proxy : %s able to use, latency : %d ms" %(proxy[t.strip()],latency)
                        conn2.commit()
                except requests.exceptions.RequestException,e:
                    print e,"proxy : %s unable to use" %proxy[t.strip()]
                    cursor.execute('delete from proxy_server where ip=%s and port=%s and type=%s',(ip,port,t.strip()))
                    conn.commit()
                    count += 1
        if count == len(type.split(','))*len(urllist):
            print "faield to test"
            cursor.execute('delete from proxy_server where ip=%s and port=%s',(ip,port))
            conn.commit()
        else:
            pass

for proxy in proxies[:2000]:
    check_proxy(proxy,*url_list)
