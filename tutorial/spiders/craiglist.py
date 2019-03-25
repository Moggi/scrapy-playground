# -*- coding: utf-8 -*-
import scrapy


class CraiglistJobsSpider(scrapy.Spider):
    name = 'craiglist_jobs'
    allowed_domains = ['newyork.craigslist.org']
    start_urls = [
        'https://newyork.craigslist.org/d/architect-engineer-cad/search/egr']

    def parse(self, response):
        listings = response.xpath('//li[@class="result-row"]')

        for listing in listings:
            link = listing.xpath(
                './/a[@class="result-title hdrlnk"]/@href').extract_first()
            yield scrapy.Request(response.urljoin(link), self.parse_jobs)

        # follow pagination links
        next_page_url = response.xpath(
            '//a[@class="button next"]/@href').extract_first()
        if next_page_url:
            yield scrapy.Request(response.urljoin(next_page_url), self.parse)

    def parse_jobs(self, response):
        title = response.xpath(
            '//span[@class="postingtitletext"]/span/text()').extract_first()

        date = response.xpath(
            '//*[@class="date timeago"]/@datetime').extract_first()

        link = response.xpath('//link[@rel="canonical"]/@href').extract_first()
        compensation = response.xpath(
            '//*[@class="attrgroup"]/span[1]/b/text()').extract_first()

        employment_type = response.xpath(
            '//*[@class="attrgroup"]/span[2]/b/text()').extract_first()

        images = response.xpath('//*[@id="thumbs"]//@src').extract()
        images = [image.replace('50x50c', '600x450') for image in images]

        description = response.xpath('//*[@id="postingbody"]/text()').extract()

        yield {
            'title': title,
            'date': date,
            'link': link,
            'images': images,
            'description': description
        }
