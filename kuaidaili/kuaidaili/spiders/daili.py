# -*- coding: utf-8 -*-
import scrapy
from kuaidaili.items import KuaidailiItem

class DailiSpider(scrapy.Spider):
    name = "daili"
    allowed_domains = ["kuaidaili.com"]
    start_urls = [
        'http://www.kuaidaili.com/free/outha/1',
    ]

    def parse(self, response):
        item = KuaidailiItem()
        item['ip'] =
        item['port'] =
        item['type'] =
        item['location'] = 
        item['latency'] = 
