import requests
from lxml import html
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from pprint import pprint

url_parse = 'https://news.mail.ru/'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.12785 YaBrowser/13.12.1599.12785 Safari/537.36'
}


def parse():
    response_main = requests.get(url_parse, headers=headers)
    dom = html.fromstring(response_main.text)
    all_links = dom.xpath("//a[contains(@class,'js-topnews__item')]/@href")
    all_links_text = dom.xpath("//li[@class='list__item']/a[@class='list__text']/@href")
    all_links.extend(all_links_text)
    result_info = []
    for link in all_links:
        result_links_info = {}
        response_links = requests.get(link, headers=headers)
        dom_link = html.fromstring(response_links.text)
        title = dom_link.xpath("//h1[@class='hdr__inner']/text()")
        content = dom_link.xpath("//div[contains(@class,'meta-speakable-intro')]/p/text()")
        author = dom_link.xpath("//a[contains(@class,'breadcrumbs__link')]/@href")
        time_publication = dom_link.xpath("//span[contains(@class,'text js-ago')]/@datetime")
        result_links_info['title'] = title[0]
        result_links_info['content'] = content[0].replace('\xa0', ' ')
        result_links_info['author'] = author[0]
        result_links_info['time_publication'] = time_publication[0]
        result_info.append(result_links_info)
        write_db(result_info)


def write_db(result):
    client = MongoClient()
    db = client['all_news']
    news = db.news
    for res in result:
        try:
            news.insert_one(res)
        except DuplicateKeyError:
            pass


parse()
