from scrapy import Spider
from tutorial.items import QuotesItem


class QuotesSpider(Spider):
    name = "quotes"
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        """Scrap all quotes from the page and follow all links"""
        for quote in response.css('div.quote'):
            author_url = quote.xpath('.//span/a/@href').extract_first()
            yield QuotesItem(
                text=quote.css('span.text::text').get(),
                author=quote.css('small.author::text').get(),
                author_url=response.urljoin(author_url),
                tags=quote.css('div.tags a.tag::text').getall(),
            )

        for _a in response.css('li.next a'):
            yield response.follow(_a, callback=self.parse)
