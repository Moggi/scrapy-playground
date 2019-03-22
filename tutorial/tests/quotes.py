import unittest
from scrapy import Request
from tutorial.items import QuotesItem
from tutorial.spiders.quotes import QuotesSpider
from tutorial.tests.responses import fake_response_from_file


class TestQuotesSpider(unittest.TestCase):

    def setUp(self):
        """Instantiate the crawler every test"""
        self.spider = QuotesSpider()

    def test_parse(self):
        """Test all itens from response"""
        test_cases = [
            'quotes.toscrape.snippet.html',
        ]
        results = self.spider.parse(fake_response_from_file(test_cases[0]))

        for item in results:
            if isinstance(item, QuotesItem):
                self.assertIsInstance(item, QuotesItem)
                self.assertIsNotNone(item['text'])
                self.assertIsNotNone(item['author'])
                self.assertIsNotNone(item['tags'])
                self.assertIsInstance(item['tags'], list)
            else:
                self.assertIsInstance(item, Request)
