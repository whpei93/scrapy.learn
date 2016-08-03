# -*- coding: utf-8 -*-
import scrapy
from proxylisty.items import proxyItem

class PlSpider(scrapy.Spider):
    name = "pl"
    allowed_domains = ["proxylisty.com"]
    start_urls = [
        'http://www.proxylisty.com/ip-proxylist-1',
    ]

    def parse(self, response):
        for a in response.xpath('//tr')[2:-2]:
            item = proxyItem()
            item['ip'] = a.xpath('.//td')[0].xpath('./text()').extract()[0].encode('utf-8')
            item['port'] = a.xpath('.//td')[1].xpath('./a/text()').extract()[0].encode('utf-8')
            yield item
