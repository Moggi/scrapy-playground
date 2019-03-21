import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ['quotes.toscrape.com']
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
    ]

    # def start_requests(self):
    #     urls = [
    #         'http://quotes.toscrape.com/page/1/',
    #         'http://quotes.toscrape.com/page/2/',
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page_name = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page_name
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
