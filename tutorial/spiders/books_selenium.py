# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.http import Request
from selenium import webdriver


class BooksSeleniumSpider(scrapy.Spider):
    name = 'books_selenium'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    def start_requests(self):
        self.driver = webdriver.Chrome('/usr/local/bin/.chromedriver')
        self.driver.get(self.start_urls[0])

        sel = Selector(text=self.driver.page_source)
        books = sel.xpath('//h3/a').extract()
        for book in books:
            url = self.start_urls[0] + book
            yield Request(url, callback=self.parse_book)

    def parse_book(self, response):
        pass
