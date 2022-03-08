import requests
import json

base_url = 'http://ws.audioscrobbler.com/2.0/'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.12785 YaBrowser/13.12.1599.12785 Safari/537.36'
}

payloads = {
    'user': USER,
    'api_key': API_COMMENT,
    'method': 'chart.getTopArtists',
    'format': 'json'
}

response = requests.get(base_url, headers=headers, params=payloads)


def json_save():
    with open('last_fm.json', 'w') as file:
        res = response.json()['artists']['artist']
        for i in res:
            json.dump(i['name'], file)
            print(i['name'])


json_save()
