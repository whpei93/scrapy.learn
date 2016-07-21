# -*- coding: utf-8 -*-
import scrapy
import time
from kuaidaili.items import KuaidailiItem

class DailiSpider(scrapy.Spider):
    name = "daili"
    allowed_domains = ["kuaidaili.com"]
    start_urls = [
        'http://www.kuaidaili.com/free/outtr/693',
        'http://www.kuaidaili.com/free/intr/640',
        'http://www.kuaidaili.com/free/inha/651',
        'http://www.kuaidaili.com/free/outha/687'
    ]
    global COUNT
    COUNT = 0
    def parse(self, response):
        for proxy_server in response.xpath('//tbody//tr'):
            try:
                item = KuaidailiItem()
                item['ip'] = proxy_server.xpath('.//td[@data-title="IP"]/text()').extract()[0].strip()
                item['port'] = proxy_server.xpath('.//td[@data-title="PORT"]/text()').extract()[0].strip()
                item['type'] = proxy_server.xpath('.//td')[3].xpath('./text()').extract()[0].strip()
                item['location'] = proxy_server.xpath('.//td')[4].xpath('./text()').extract()[0].strip()
                item['latency'] = proxy_server.xpath('.//td')[5].xpath('./text()').extract()[0].strip()
                yield item
            except:
                pass
        if response.status==200:
            global COUNT
            COUNT += 1
            if COUNT == 10:
                time.sleep(10)
                COUNT = 0
                url = response.url[:len(response.url)-len(response.url.split('/')[-1])]+str(int(response.url.split('/')[-1])+1)
                yield scrapy.Request(url, callback=self.parse)
            else:
                url = response.url[:len(response.url)-len(response.url.split('/')[-1])]+str(int(response.url.split('/')[-1])+1)
                yield scrapy.Request(url,callback=self.parse)
        else:
            print "page error..."

