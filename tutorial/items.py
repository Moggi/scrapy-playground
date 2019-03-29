# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QuotesItem(scrapy.Item):
    text = scrapy.Field()
    author = scrapy.Field()
    author_url = scrapy.Field()
    tags = scrapy.Field()


class BooksItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    rating = scrapy.Field()
    description = scrapy.Field(serializer=str)
    upc = scrapy.Field()
    product_type = scrapy.Field()
    price_without_tax = scrapy.Field()
    price_with_tax = scrapy.Field()
    tax = scrapy.Field()
    availability = scrapy.Field()
    number_of_review = scrapy.Field()


class AuthorsItem(scrapy.Item):
    name = scrapy.Field()
    birthdate = scrapy.Field()
    bio = scrapy.Field(serializer=str)
