import scrapy
from scrapy.http import HtmlResponse
from leroymerlin.items import LeroymerlinItem
from scrapy.loader import ItemLoader


class LeroymerlinparseSpider(scrapy.Spider):
    name = 'leroymerlinparse'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f'https://leroymerlin.ru/search/?q={kwargs.get("search")}']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@data-qa-pagination-item='right']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//a[@data-qa='product-image']")
        for link in links:
            yield response.follow(link, callback=self.parse_file)

    def parse_file(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroymerlinItem(), response=response)
        loader.add_xpath('title', "//h1[@slot='title']/text()")
        loader.add_xpath('price', "//uc-pdp-price-view[@slot='primary-price']/span/text()")
        loader.add_xpath('currency', "//uc-pdp-price-view[@slot='primary-price']/span/text()")
        loader.add_value('url', response.url)
        loader.add_xpath('photos', "//source[contains(@media,'(min-width: 1024px)')]/@srcset")
        yield loader.load_item()
