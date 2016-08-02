#!/usr/bin/python
# coding:utf-8

import requests
from bs4 import BeautifulSoup

start_urls=['http://www.xicidaili.com/wt/1']

headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'}

def get_page(url):
    res = requests.get('http://www.xicidaili.com/wt/1',headers=headers)
    return res.text

def parse(page):
    soup = BeautifulSoup(page)
    print soup.td

a = get_page(start_urls[0])
soup = BeautifulSoup(a)
for i in soup.body.children:
    print i


