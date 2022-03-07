# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class ParseBookPipeline:
    def __init__(self):
        client = MongoClient('127.0.0.1', 27017)
        self.mongoclient = client.labirint_book

    def process_item(self, item, spider):
        item['authors'] = ','.join(item['authors'])


        collection = self.mongoclient['labirint']
        collection.insert_one(item)
        # return item
