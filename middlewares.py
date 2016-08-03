# -*- coding: utf-8 -*-

import random

class proxyMiddleware(object):
    def __init__(self, setting):
        self.proxy_list = setting.get('PROXY_LIST')
        with open(self.proxy_list,'r') as f:
            self.proxies = [ip.strip() for ip in f]

    def parse_request(self, request, spider):
        request.meta['proxy'] = 'http://{}'.format(random.choice(self.proxies))