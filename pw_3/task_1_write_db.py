from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import requests
from bs4 import BeautifulSoup
from pprint import pprint

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.12785 YaBrowser/13.12.1599.12785 Safari/537.36'
}
base_url = 'https://nn.hh.ru/'

request_user = input('Введите запрос: ')
result_list = []

client = MongoClient()
db = client['all_vacancy']


def vacancy_parse(page):
    global last_page
    for count in range(page):
        params = {'text': request_user,
                  'page': count}
        url = f'https://nn.hh.ru/search/vacancy?search_field=name&search_field=company_name&search_field=description&text=&page=0&hhtmFrom=vacancy_search_list'
        response = requests.get(url, headers=headers, params=params)
        dom = BeautifulSoup(response.text, 'html.parser')
        count_page = dom.find_all('a', {'data-qa': 'pager-page'})[-1]
        last_page = int(count_page.get_text())
        data_parse = dom.select('div.vacancy-serp-item')
        for data in data_parse:
            vacancy_name = data.find('a', {'class': 'bloko-link'})
            title_vacancy = vacancy_name.get_text()
            link_vacancy = vacancy_name['href']
            vacancy_dict = {}
            vacancy_dict['_id'] = link_vacancy + '1'
            vacancy_dict['base_url'] = base_url
            vacancy_dict['vacancy_title'] = title_vacancy
            vacancy_dict['vacancy_link'] = link_vacancy
            data_money = data.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
            dict_money = {}
            if data_money:
                data_money = data_money.get_text().replace('\u202f', '')
                data_list_money = data_money.split()
                dict_money['currency'] = data_list_money[-1]
                if data_money.startswith('от'):
                    dict_money['min_salary'] = int(data_list_money[1])
                elif data_money.startswith('до'):
                    dict_money['max_salary'] = int(data_list_money[1])
                elif len(data_list_money) == 4:
                    dict_money['min_salary'] = int(data_list_money[0])
                    dict_money['max_salary'] = int(data_list_money[2])
            else:
                dict_money['min_salary'] = None
                dict_money['max_salary'] = None
                dict_money['currency'] = None
            vacancy_dict['salary'] = dict_money
            result_list.append(vacancy_dict)

    write_to_db(result_list)


def write_to_db(result):
    print(len(result))
    vacancy = db.vacancy_info
    for res in result:
        try:
            vacancy.insert_one(res)
        except DuplicateKeyError:
            pass
    sample_to_base(vacancy)


def sample_to_base(vacancy):
        entered_value = int(input('Введите значение: '))
        for vac in vacancy.find({'$or': [{'salary.min_salary': {'$gt': entered_value}},
                                         {'salary.max_salary': {'$gt': entered_value}}]}):
            pprint(vac)



params = {'text': request_user}
url = f'https://nn.hh.ru/search/vacancy?search_field=name&search_field=company_name&search_field=description&text=&page=0&hhtmFrom=vacancy_search_list'
response = requests.get(url, headers=headers, params=params)
dom = BeautifulSoup(response.text, 'html.parser')
count_page = dom.find_all('a', {'data-qa': 'pager-page'})[-1]
last_page = int(count_page.get_text())
vacancy_parse(last_page)
