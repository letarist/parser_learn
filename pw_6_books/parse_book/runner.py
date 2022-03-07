from scrapy.settings import Settings
from scrapy.crawler import CrawlerProcess

from parse_book.spiders.labirint import LabirintSpider
from parse_book.spiders.book24 import Book24Spider
from parse_book import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    # process.crawl(LabirintSpider)
    process.crawl(Book24Spider)


    process.start()
