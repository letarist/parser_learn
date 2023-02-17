import requests
import json

username = input('Введите логин с Github: ').lower()
url = f'https://api.github.com/users/{username}/repos'

response = requests.get(url)
with open('repos.json', 'w') as file:
    for names in response.json():
        json.dump(names['name'], file)

count = 1
for i in response.json():
    print(f'{count}: Имя репозитория: {i["name"]}')
    count += 1
