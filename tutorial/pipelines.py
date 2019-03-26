# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
from pymongo import MongoClient
from scrapy.conf import settings


class BooksImagePipeline(object):
    """Pipeline to rename each item image"""

    def process_item(self, item, spider):
        """Process item to rename its image name"""
        os.chdir(settings['IMAGES_STORE'])

        if len(item['images']):
            new_image_name = 'full/' + item['title'][0] + '.jpeg'
            os.rename(item['images'][0]['path'], new_image_name)

        return item


class MongoDBPipeline(object):
    """Pipeline to save each result into mongodb"""

    def __init__(self):
        connection = MongoClient(settings['MONGODB_URI'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item
