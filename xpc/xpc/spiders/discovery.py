# -*- coding: utf-8 -*-
import scrapy


class DiscoverySpider(scrapy.Spider):
    name = 'discovery'
    allowed_domains = ['www.xinpianchang.com']
    start_urls = ['http://www.xinpianchang.com/']

    def parse(self, response):
        pass
