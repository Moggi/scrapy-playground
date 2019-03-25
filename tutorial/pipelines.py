# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
from tutorial import settings


class BooksImagePipeline(object):
    """Pipeline to rename each item image"""
    def process_item(self, item, spider):
        """Process item to rename its image name"""
        os.chdir(settings.IMAGES_STORE)

        if len(item['images']):
            new_image_name = 'full/' + item['title'][0] + '.jpeg'
            os.rename(item['images'][0]['path'], new_image_name)

        return item
