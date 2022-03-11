from scrapy.settings import Settings
from scrapy.crawler import CrawlerProcess

from leroymerlin import settings
from leroymerlin.spiders.leroymerlinparse import LeroymerlinparseSpider

if __name__ == '__main__':
    spider_settings = Settings()
    spider_settings.setmodule(settings)

    process = CrawlerProcess(spider_settings)
    process.crawl(LeroymerlinparseSpider)

    process.start()
