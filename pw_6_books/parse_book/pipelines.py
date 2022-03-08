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
        self.mongoclient = client.book

    def process_item(self, item, spider):
        item['rate'] = item['rate'].strip().replace(',', '.')
        item['rate'] = float(item['rate'])
        if item['price'] is not None and item['price_sale'] is not None:
            item['price'] = item['price'].replace('₽', '').strip().replace('\xa0', '')
            item['price'] = int(item['price'])
            item['price_sale'] = item['price_sale'].replace('₽', '').strip().strip().replace('\xa0', '')
            item['price_sale'] = int(item['price_sale'])
        if spider.name == 'labirint':
            collection = self.mongoclient['labirint']
            collection.insert_one(item)
        elif spider.name == 'book24':
            collection = self.mongoclient['book24']
            collection.insert_one(item)
