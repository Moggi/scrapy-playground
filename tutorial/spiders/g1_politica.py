# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy import Spider
from scrapy.http import Request
from datetime import datetime


class G1PoliticaSpider(Spider):
    name = 'g1_politica'
    allowed_domains = ['g1.globo.com']
    start_urls = ['https://g1.globo.com/politica/']

    def parse(self, response):
        posts = response.xpath(
            '//*[contains(@class, "feed-post")]//*[@class="feed-post-body"]')

        for post in posts:
            post_info = post.xpath(
                './/*[contains(@class, "feed-post-body-title")]')

            title = post_info.xpath('.//a/text()').extract_first()
            url = post_info.xpath('.//a/@href').extract_first()
            ago_time = post.xpath(
                './/*[@class="feed-post-datetime"]/text()').extract_first()
            time = datetime.now().isoformat()

            yield {
                'title': title,
                'url': url,
                'ago_time': ago_time,
                'time': time,
            }
