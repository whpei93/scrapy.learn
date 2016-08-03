# -*- coding: utf-8 -*-
import scrapy
import time
from xici.items import proxyItem
class XcSpider(scrapy.Spider):
    name = "xc"
    allowed_domains = ["xicidaili.com"]
    start_urls = [
        'http://www.xicidaili.com/nn/74',
        'http://www.xicidaili.com/nt/66',
        'http://www.xicidaili.com/wn/59',
        'http://www.xicidaili.com/wt/62'
    ]

    def __init__(self):
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'}

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        for tr in response.xpath('//tr')[1:]:
            try:
                item = proxyItem()
                item['ip'] = tr.xpath('./td')[1].xpath('./text()').extract()[0].strip()
                item['port'] = tr.xpath('./td')[2].xpath('./text()').extract()[0].strip()
                yield item
            except:
                pass
        if (response.status == 200) & (len(response.xpath('//tr')) > 15):
            url = response.url[:len(response.url)-len(response.url.split('/')[-1])]+str(int(response.url.split('/')[-1])+1)
            print url
            yield scrapy.Request(url, headers=self.headers, callback=self.parse)
        else:
            print 'Error Page...'
