import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        """Scrap all quotes from the page and follow all links"""
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }

        # for _a in response.css('li.next a'):
        #     yield response.follow(_a, callback=self.parse)
