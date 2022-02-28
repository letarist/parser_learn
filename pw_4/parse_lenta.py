from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from requests import request
from lxml import html

base_url = ''
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.12785 YaBrowser/13.12.1599.12785 Safari/537.36'
}
