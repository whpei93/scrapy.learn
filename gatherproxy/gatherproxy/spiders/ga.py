# -*- coding: utf-8 -*-
import scrapy
from gatherproxy.items import proxyItem

class GaSpider(scrapy.Spider):
    name = "ga"
    allowed_domains = ["gatherproxy.com"]
    start_urls = [
        'http://www.gatherproxy.com/proxyserverlistbyport'
    ]

    def parse(self, response):
        for a in response.xpath('//li'):
            if len(a.xpath('./a/@href').extract()) == 1:
                if 'proxylist/port' in a.xpath('./a/@href').extract()[0].encode('utf-8'):
                    port = a.xpath('./a/@href').extract()[0].encode('utf-8').split('/')[-1]
                    formdata = {'Port':port, 'PageIdx':'10'}
                    url = 'http://www.gatherproxy.com/'+a.xpath('./a/@href').extract()[0].encode('utf-8')
                    yield scrapy.http.FormRequest(url, formdata=formdata, callback=self.sub_parse)

    def sub_parse(self, response):
        try :
            current_index = response.xpath('//span[@class="current"]/text()').extract()[0]
            end_index = response.xpath('//a[@class="inactive"]')[-1].xpath('./@href').extract()[0].strip('#')
            if int(current_index) < int(end_index):
                formdata = {'Port':response.url.split('/')[-1], 'PageIdx':str(int(current_index)+1)}
                yield scrapy.http.FormRequest(response.url, formdata=formdata, callback=self.sub_parse)
        except:
            pass
        for a in response.xpath('//tr')[2:]:
            item = proxyItem()
            item['ip'] = a.xpath('.//script').xpath('./text()').extract()[0].encode('utf-8').strip().split('(')[-1].rstrip(')')
            item['port'] = response.url.split('/')[-1]
            yield item
