#!/usr/bin/python
# coding:utf-8

import mysql.connector
import requests
import threading
import sys

if len(sys.argv) == 1:
    test_domain = raw_input('Please input target domain :')
else :
    test_domain = sys.argv[1]
url_list = {'douban': 'https://www.douban.com/', 't66y': 'http://t66y.com/index.php'}
web_length = {'douban':80000, 't66y':14000}

# DB info
DB_HOST = "192.168.1.108"
DB_USER = "root"
DB_PASS = "PEter)()3"


# SQL
clean_tmp = 'delete from proxy where id not in (select * from (select max(id) from proxy group by ip,port) as b)'
clean_valid = 'delete from proxy where id not in (select * from (select max(id) from proxy group by ip,port,type,domain) as b)'
delete_unable = 'delete from proxy where id=%s'
insert_able = 'insert into proxy (id,ip,port,type,latency,domain) values(null,%s,%s,%s,%s,%s)'
get_proxy = 'select ip,port,id from proxy limit 100'

# Operate MySql
def op_db(host,dbname,user,passwd,sql,*list):
    conn = mysql.connector.connect(user=user, password=passwd, database=dbname, host=host, use_unicode=True)
    cursor = conn.cursor()
    if sql.startswith('select'):
        cursor.execute(sql)
        return cursor.fetchall()
    elif sql.startswith('insert'):
        cursor.execute(sql, list)
        conn.commit()
    elif sql.startswith('delete'):
        cursor.execute(sql, list)
        conn.commit()
    else:
        cursor.execute(sql)
        conn.commit()

# Run this
op_db(DB_HOST, "kuaidaili", DB_USER, DB_PASS, clean_tmp)
tmp_servers = op_db(DB_HOST, "kuaidaili", DB_USER, DB_PASS, get_proxy)

# Check proxy
def check_proxy(url):
    types = ['http', 'https']
    servers = []
    for i in range(400):
        try:
            servers.append(tmp_servers.pop(0))
        except:
            pass
    for server in servers:
        for t in types:
            proxy = {}
            proxy[t] = t + '://' + str(server[0]) + ':' + str(server[1])
            try:
                res = requests.get(url, proxies=proxy, timeout=5)
                if (res.status_code == 200) and (res.url == url) and (len(res.text) > web_length[test_domain]):
                    latency = res.elapsed.microseconds / 1000
                    print proxy[t], latency, 'is able to access', res.url
                    op_db(DB_HOST, test_domain, DB_USER, DB_PASS, insert_able, str(server[0]), str(server[1]), t, str(latency), url.split('/')[-2].split('.')[-2])
                else:
                    pass
            except requests.HTTPError, requests.ConnectionError:
                pass
            except :
                pass

# Main function
def main():
    thread_list = []
    for i in range(100):
        t = threading.Thread(target=check_proxy, args=(url_list[test_domain],))
        thread_list.append(t)
        t.start()
    for t in thread_list:
        t.join()
    op_db(DB_HOST, test_domain, DB_USER, DB_PASS, clean_valid)

if __name__ == '__main__':
    main()

