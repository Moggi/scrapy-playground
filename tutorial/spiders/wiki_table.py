# -*- coding: utf-8 -*-
import scrapy


class WikiTableSpider(scrapy.Spider):
    name = 'wiki_table'
    allowed_domains = ['en.wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/\
        List_of_United_States_cities_by_population']

    def parse(self, response):
        table = response.xpath(
            '//table[@class="wikitable sortable"]')[0]
        trs = table.xpath('.//tr')[1:]
        for tr in trs:
            rank = tr.xpath('.//td[1]/text()').extract_first()
            # @FIXME: no pattern on city name column
            name = ''.join(tr.xpath('.//td[2]//a/text()').extract())
            # @FIXME: no pattern on state column
            state = ''.join(tr.xpath('.//td[3]//text()').extract)

            yield {
                'rank': rank,
                'name': name,
                'state': state,
            }
