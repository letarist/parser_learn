import scrapy
from scrapy.http import HtmlResponse


class Book24Spider(scrapy.Spider):
    name = 'book24'
    allowed_domains = ['book24.ru']

    start_urls = [
        f'https://book24.ru/search/page-1/?q=%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5']

    # f'https://book24.ru/search/page-{count}/?q=%D1%88%D0%BA%D0%BE%D0%BB%D0%B0']

    def parse(self, response: HtmlResponse):
        count = 1
        while True:
            if response.status == 200:
                yield response.follow(
                    f'https://book24.ru/search/page-{count + 1}/?q=%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5',
                    callback=self.parse)
                count += 1
            else:
                break
        links = response.xpath("//a[@class='product-title-link']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.book_info)

    def book_info(self):
        pass
