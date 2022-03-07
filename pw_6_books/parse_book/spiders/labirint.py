import scrapy
from scrapy.http import HtmlResponse
from parse_book.items import ParseBookItem


class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/%D0%9A%D0%BB%D0%B0%D1%81%D1%81%D0%B8%D0%BA%D0%B0/?stype=0',
                  'https://www.labirint.ru/search/%D0%9A%D0%BB%D0%B0%D1%81%D1%81%D0%B8%D0%BA%D0%B0/?stype=0&available=1&wait=1&no=1&paperbooks=1&ebooks=1&otherbooks=1&russianonly=1']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@class='pagination-next__text']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//a[@class='cover']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.book_info)

    def book_info(self, response: HtmlResponse):
        title = response.xpath('//h1/text()').get()
        authors = response.xpath("//div[text()='Автор: ']/a/text()").getall()
        price = response.xpath("//span[@class = 'buying-priceold-val-number']/text()").get()
        price_sale = response.xpath("//div[@class = 'buying-pricenew-val']/span/text()").get()
        rate = response.xpath("//div[@class='left']//text()").getall()[1]
        yield ParseBookItem(title=title, authors=authors, price=price, price_sale=price_sale, rate=rate)
