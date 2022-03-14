# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient


class LeroymerlinPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongoclient = client.goods

    def process_item(self, item, spider):
        if spider.name == 'leroymerlinparse':
            collection = self.mongoclient['LMGoods']
            collection.insert_one(item)
        return item


class LeroyPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for photo in item['photos']:
                try:
                    yield scrapy.Request(photo)
                except Exception:
                    print(Exception)

    def item_completed(self, results, item, info):
        item['photos'] = [i[1] for i in results if i[0]]
        return item
