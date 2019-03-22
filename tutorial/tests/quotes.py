import unittest
from spiders.quotes import QuotesSpider
from tests.responses import fake_response_from_file


class TestQuotesSpider(unittest.TestCase):

    def setUp(self):
        """Instantiate the crawler every test"""
        self.spider = QuotesSpider()

    def test_parse(self):
        """Test all itens from response"""
        s = [
            'quotes.toscrape.snippet.html',
        ]
        results = self.spider.parse(fake_response_from_file(s[0]))
        for item in results:
            self.assertIsNotNone(item['text'])
            self.assertIsNotNone(item['author'])
            self.assertIsNotNone(item['tags'])
            self.assertIsInstance(item['tags'], list)
