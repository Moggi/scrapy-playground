import unittest
from scrapy import Request
from tutorial.items import BooksItem
from tutorial.spiders.books import BooksSpider
from tutorial.tests.responses import fake_response_from_file


class TestBooksSpider(unittest.TestCase):

    def setUp(self):
        """Instantiate the crawler every test"""
        self.spider = BooksSpider()

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
                title='A Light in the Attic',
                price='£51.77',
                image_url=(
                    f'''http://books.toscrape.com/media/cache/fe/72/fe72f053'''
                    f'''2301ec28892ae79a629a293c.jpg'''
                ),
                rating='Three',
                description=(
                    f'''It's hard to imagine a world without A Light in '''
                    f'''the Attic. This now-classic collection of poetry '''
                    f'''and drawings ...'''
                )
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
