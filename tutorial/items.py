# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QuotesItem(scrapy.Item):
    text = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()


class BooksItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    image_url = scrapy.Field()
    rating = scrapy.Field()
    description = scrapy.Field(serializer=str)
