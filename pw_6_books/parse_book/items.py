# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ParseBookItem(scrapy.Item):
    title = scrapy.Field()
    authors = scrapy.Field()
    price = scrapy.Field()
    price_sale = scrapy.Field()
    rate = scrapy.Field()
    _id = scrapy.Field()
