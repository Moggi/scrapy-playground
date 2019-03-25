import unittest
from scrapy import Request
from tutorial.items import BooksItem
from tutorial.spiders.books import BooksSpider
from tutorial.tests.responses import fake_response_from_file


class TestBooksSpider(unittest.TestCase):

    def setUp(self):
        """Instantiate the crawler every test"""
        self.spider = BooksSpider(category='http://books.toscrape.com/')

    def test_parse(self):
        """Test it we only get Request objects"""
        page = 'books.toscrape.snippet.html'
        results = self.spider.parse(fake_response_from_file(page))

        for item in results:
            self.assertIsInstance(item, Request)

    def test_parse_book(self):
        """Test extraction of itens from parse_book"""
        page = 'book1.toscrape.snippet.html'
        test_cases = [
            BooksItem(
                title=['A Light in the Attic'],
                price=['£51.77'],
                image_urls=[''],
                rating=['Three'],
                description=[(
                    f'''It's hard to imagine a world without A Light in '''
                    f'''the Attic. This now-classic collection of poetry '''
                    f'''and drawings ...'''
                )],
                upc=['a897fe39b1053632'],
                product_type=['Books'],
                price_without_tax=['£51.77'],
                price_with_tax=['£51.77'],
                tax=['£0.00'],
                availability=['In stock (22 available)'],
                number_of_review=['0']
            )
            # BooksItem(''),
        ]
        html_content = fake_response_from_file(
            page,
            'http://books.toscrape.com'
        )
        results = self.spider.parse_book(html_content)

        for item in results:
            self.assertIsInstance(item, BooksItem)
            self.assertDictEqual(dict(item), dict(test_cases[0]))
