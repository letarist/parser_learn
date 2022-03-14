# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import Compose, MapCompose, TakeFirst


def correct_price(arg):
    try:
        res = int(arg[0].replace(' ', ''))
        return res
    except Exception:
        return arg[0]


def correct_currency(arg):
    try:
        res = arg[1]
        return res
    except Exception:
        return arg[1]


class LeroymerlinItem(scrapy.Item):
    _id = scrapy.Field()
    title = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=Compose(correct_price), output_processor=TakeFirst())
    currency = scrapy.Field(input_processor=Compose(correct_currency), output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
