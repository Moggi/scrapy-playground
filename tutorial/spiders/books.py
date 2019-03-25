import scrapy
from scrapy.http import Request
from tutorial.items import BooksItem


class BooksSpider(scrapy.Spider):
    """Simple spider to extract books from books.toscrape.com"""
    name = 'books'
    allowed_domains = ['books.toscrape.com']

    def __init__(self, category=None):
        """Initiate the spider with a specific category or the default url"""
        super().__init__()
        self.start_urls = ['http://books.toscrape.com/']
        if category:
            self.start_urls = [category]

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

        # product information data points
        upc = self.product_info(response, 'UPC')
        product_type = self.product_info(response, 'Product Type')
        price_without_tax = self.product_info(response, 'Price (excl. tax)')
        price_with_tax = self.product_info(response, 'Price (incl. tax)')
        tax = self.product_info(response, 'Tax')
        availability = self.product_info(response, 'Availability')
        number_of_review = self.product_info(response, 'Number of reviews')

        yield BooksItem(
            title=title,
            price=price,
            image_url=image_absolute_url,
            rating=rating,
            description=description,
            upc=upc,
            product_type=product_type,
            price_without_tax=price_without_tax,
            price_with_tax=price_with_tax,
            tax=tax,
            availability=availability,
            number_of_review=number_of_review
        )

    @staticmethod
    def product_info(response, value):
        """Extract the well defined Product Information"""
        return response.xpath(
            f'//th[text()="{value}"]/following-sibling::td/text()'
        ).extract_first()
