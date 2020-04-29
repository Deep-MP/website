# -*- coding: utf-8 -*-
import scrapy


class DeepmpSpider(scrapy.Spider):
    name = 'deepmp'
    allowed_domains = ['deepmp.com']
    start_urls = ['http://deepmp.com/']

    def parse(self, response):
        pass
