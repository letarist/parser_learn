import scrapy
from scrapy.http import HtmlResponse
from parse_book.items import ParseBookItem


class Book24Spider(scrapy.Spider):
    name = 'book24'
    allowed_domains = ['book24.ru']
    count = 1
    links_book = []

    start_urls = [
        'https://book24.ru/search/?q=%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5']

    # f'https://book24.ru/search/page-{count}/?q=%D1%88%D0%BA%D0%BE%D0%BB%D0%B0']

    def parse(self, response: HtmlResponse):
        if response.status == 200:
            next_page = f'https://book24.ru/search/page-{self.count}/?q=%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5'
            self.count += 1
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath(
            "//div[@class='product-list__item']//a[contains(@class,'product-card__name smartLink')]/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.book_info)

    def book_info(self, response: HtmlResponse):
        title = response.xpath("//h1[@itemprop]/text()").get()
        authors = response.xpath("//div[@class='product-characteristic__value']//text()").get()
        price = response.xpath("//span[contains(@class,'product-sidebar-price__price')]/text()").get()
        price_sale = response.xpath("//div[@itemprop='offers']/span[contains(@class,'app-price')]/text()").get()
        rate = response.xpath("//span[@class='rating-widget__main-text']/text()").get()
        yield ParseBookItem(title=title, authors=authors, price=price, price_sale=price_sale, rate=rate)
