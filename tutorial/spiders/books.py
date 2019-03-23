import scrapy
from scrapy.http import Request


class BooksSpider(scrapy.Spider):
    """Simple spider to extract books from books.toscrape.com"""
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        books = response.xpath('//h3/a/@href').extract()
        for book in books:
            absolute_url = response.urljoin(book)
            yield Request(absolute_url, callback=self.parse_book)

        # process next page
        next_page_url = response.xpath(
            '//a[text()="next"]/@href').extract_first()
        next_page_url_absolute = response.urljoin(next_page_url)
        yield Request(next_page_url_absolute)

    def parse_book(self, response):
        yield {
            '': ''
        }
