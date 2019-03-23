import scrapy
from scrapy.http import Request
from tutorial.items import BooksItem


class BooksSpider(scrapy.Spider):
    """Simple spider to extract books from books.toscrape.com"""
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        """Grab all book pages and follow them"""
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
        """Extract each book info"""
        title = response.css('h1::text').extract_first()
        price = response.xpath(
            '//*[@class="price_color"]/text()').extract_first()

        image_url = response.xpath('//img/@src').extract_first()
        image_absolute_url = response.urljoin(image_url)

        rating = response.xpath(
            '//*[contains(@class, "star-rating")]/@class').extract_first()
        rating = rating.replace('star-rating ', '')

        description = response.xpath(
            '//*[@id="product_description"]/following-sibling::p/text()'
        ).extract_first()

        yield BooksItem(
            title=title,
            price=price,
            image_url=image_absolute_url,
            rating=rating,
            description=description
        )
