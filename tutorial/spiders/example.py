# -*- coding: utf-8 -*-
import scrapy


class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['example.com']
    start_urls = ['http://example.com/']

    def parse(self, response):
        self.log('[Start Parsing] {}'.format('#'*26))
        page_title = response.xpath('//title/text()').extract_first()
        # page_title = response.css('title::text').get()
        self.log(f'[Parsing:] {page_title}')
        pass
