# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request
from datetime import datetime


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
        time_published = response.xpath(
            '//meta[@property="article:published_time"]/@content'
        ).extract_first()
        description = response.xpath(
            '//meta[@name="description"]/@content').extract_first()

        content = response.xpath(
            '//*[@class="entry-content"]//following-sibling::p/text()'
        ).extract()
        content = '\n'.join(content)

        author_name = response.xpath(
            '//*[@class="author-bio__name"]/a/@title').extract_first()
        author_link = response.xpath(
            '//*[@class="author-bio__name"]/a/@href').extract_first()
        yield {
            'title': title,
            'url': url,
            'time_published': time_published,
            'description': description,
            'content': content,
            'author': author_name,
            'author_link': author_link,
        }
