import json

import requests
from bs4 import BeautifulSoup

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.12785 YaBrowser/13.12.1599.12785 Safari/537.36'
}
base_url = 'https://nn.hh.ru/'

request_user = input('Введите запрос: ')


def base_request(request_user):
    url = f'https://nn.hh.ru/search/vacancy?search_field=name&search_field=company_name&search_field=description&text={request_user}&from=suggest_post'
    response = requests.get(url, headers=headers)
    return BeautifulSoup(response.text, 'html.parser')


result_list = []


def vacancy_parse(page):
    dom = base_request(request_user)
    data_parse = dom.select('div.vacancy-serp-item')
    for count in range(page):
        for data in data_parse:
            vacancy_name = data.find('a', {'class': 'bloko-link'})
            title_vacancy = vacancy_name.get_text()
            link_vacancy = vacancy_name['href']
            data_money = data.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
            vacancy_dict = {}
            dict_money = {}
            if data_money:
                data_money = data_money.get_text().replace('\u202f', '')

                data_list_money = data_money.split()
                dict_money['currency'] = data_list_money[-1]
                if data_money.startswith('от'):
                    dict_money['min_salary'] = data_list_money[1]
                elif data_money.startswith('до'):
                    dict_money['max_salary'] = data_list_money[1]
                elif len(data_list_money) == 4:
                    dict_money['min_salary'] = data_list_money[0]
                    dict_money['max_salary'] = data_list_money[2]
            else:
                dict_money['min_salary'] = None
                dict_money['max_salary'] = None
                dict_money['currency'] = None
            vacancy_dict['base_url'] = base_url
            vacancy_dict['vacancy_title'] = title_vacancy
            vacancy_dict['vacancy_link'] = link_vacancy
            vacancy_dict['salary'] = dict_money
            result_list.append(vacancy_dict)
    write_to_file(result_list)


def write_to_file(result):
    with open('parse_hh.json', 'w') as file:
        for res in result:
            json.dump(res, file)


dom = base_request(request_user)
count_page = dom.find_all('a', {'data-qa': 'pager-page'})[-1]
last_page = int(count_page.get_text())
vacancy_parse(last_page)
