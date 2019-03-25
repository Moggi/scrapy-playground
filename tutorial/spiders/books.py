# import os
# import glob
from scrapy import Spider
from scrapy.http import Request
from scrapy.loader import ItemLoader
from tutorial.items import BooksItem


class BooksSpider(Spider):
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
        # next_page_url = response.xpath(
        #     '//a[text()="next"]/@href').extract_first()
        # next_page_url_absolute = response.urljoin(next_page_url)
        # yield Request(next_page_url_absolute)

    def parse_book(self, response):
        """Extract each book info"""
        item_loader = ItemLoader(item=BooksItem(), response=response)

        item_loader.add_value(
            'title', response.css('h1::text').extract_first())

        item_loader.add_value(
            'price', response.xpath(
                '//*[@class="price_color"]/text()').extract_first())

        image_url = response.xpath('//img/@src').extract_first()
        item_loader.add_value(
            'image_urls', response.urljoin(image_url) if image_url else '')

        rating = response.xpath(
            '//*[contains(@class, "star-rating")]/@class').extract_first()
        item_loader.add_value(
            'rating', rating.replace('star-rating ', ''))

        item_loader.add_value(
            'description', response.xpath(
                '//*[@id="product_description"]/following-sibling::p/text()'
            ).extract_first())

        # product information data points
        item_loader.add_value(
            'upc', self.product_info(response, 'UPC'))
        item_loader.add_value(
            'product_type', self.product_info(response, 'Product Type'))
        item_loader.add_value(
            'price_without_tax',
            self.product_info(response, 'Price (excl. tax)'))
        item_loader.add_value(
            'price_with_tax', self.product_info(response, 'Price (incl. tax)'))
        item_loader.add_value(
            'tax', self.product_info(response, 'Tax'))
        item_loader.add_value(
            'availability', self.product_info(response, 'Availability'))
        item_loader.add_value(
            'number_of_review',
            self.product_info(response, 'Number of reviews'))

        yield item_loader.load_item()

    @staticmethod
    def product_info(response, value):
        """Extract the well defined Product Information"""
        return response.xpath(
            f'//th[text()="{value}"]/following-sibling::td/text()'
        ).extract_first()

    # def close(self, reason):
    #     csv_file = max(glob.iglob('*.csv'), key=os.path.getctime)
    #     os.rename(csv_file, 'foobar.csv')
