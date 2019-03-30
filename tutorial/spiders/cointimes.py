# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request


class CointimesSpider(Spider):
    """A spider to extract cointimes posts"""
    name = 'cointimes'
    allowed_domains = ['cointimes.com.br']
    start_urls = ['https://cointimes.com.br']

    def parse(self, response):
        """Extract all posts from a page"""
        featured_posts = response.xpath(
            '//*[@class="card-picture__thumb"]/@href').extract()
        for url in featured_posts:
            yield Request(url, callback=self.parse_post)

        normal_posts = response.xpath(
            '//*[@class="card-default__thumb"]/@href').extract()
        for url in normal_posts:
            yield Request(url, callback=self.parse_post)

    def parse_post(self, response):
        """Extract posts information"""
        title = response.xpath(
            '//*[@class="head-page__title"]/text()').extract_first()
        url = response.xpath(
            '//link[@rel="canonical"]/@href').extract_first()
        description = response.xpath(
            '//meta[@name="description"]/@content').extract_first()

        content = response.xpath(
            '//*[@class="entry-content"]//following-sibling::p/text()'
        ).extract()
        content = '\n'.join(content)
        yield {
            'title': title,
            'url': url,
            'description': description,
            'content': content,
        }
