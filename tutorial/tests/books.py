import unittest
from scrapy import Request
from tutorial.spiders.books import BooksSpider
from tutorial.tests.responses import fake_response_from_file


class TestBooksSpider(unittest.TestCase):

    def setUp(self):
        """Instantiate the crawler every test"""
        self.spider = BooksSpider()

    def test_parse(self):
        """Test it we only get Request objects"""
        test_cases = [
            'books.toscrape.snippet.html',
        ]
        results = self.spider.parse(fake_response_from_file(test_cases[0]))

        for item in results:
            self.assertIsInstance(item, Request)

    def test_parse_book(self):
        """Test extraction of itens from parse_book"""
        test_cases = [
            'books.toscrape.snippet.html',
        ]
        html_content = fake_response_from_file(test_cases[0])
        results = self.spider.parse_book(html_content)

        for item in results:
            self.assertIsInstance(item, dict)
