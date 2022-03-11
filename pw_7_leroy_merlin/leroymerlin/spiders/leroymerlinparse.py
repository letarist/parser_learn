import scrapy
from scrapy.http import HtmlResponse
from leroymerlin.items import LeroymerlinItem


class LeroymerlinparseSpider(scrapy.Spider):
    name = 'leroymerlinparse'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['https://leroymerlin.ru/search/?q=%D0%9B%D0%BE%D0%BF%D0%B0%D1%82%D0%B0']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@data-qa-pagination-item='right']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//a[@data-qa='product-image']")
        for link in links:
            yield response.follow(link, callback=self.parse_file)

    def parse_file(self, response: HtmlResponse):
        title = response.xpath("//h1[@slot='title']/text()").get()
        price = response.xpath("//uc-pdp-price-view[@slot='primary-price']/span/text()").getall()
        url = response.url
        yield LeroymerlinItem(title=title, price=price, url=url)
