from pprint import pprint
import requests
import json
import time
from tqdm import tqdm

with open('token.txt', 'r') as file_object:
    vk_token = file_object.read().strip()


def get_headers_ya():
    return {
        'Content-Type': 'application/json',
        'Authorization': f'OAuth {ya_token}'
    }


def create_folder(name):
    uri = 'https://cloud-api.yandex.net/v1/disk/resources'
    requests.put(f'{uri}?path={name}', headers=get_headers_ya())


id_vk = str(input('Введите ID пользователя в ВК: '))
ya_token = str(input('Введите токен для Я.Диска: '))

URL = 'https://api.vk.com/method/photos.get'
params = {
    'user_id': id_vk,
    'access_token': vk_token,
    'v': '5.131',
    'album_id': 'profile',
    'extended': '1',
    'photo_sizes': '1',
    'count': 50
}
res = requests.get(URL, params=params)
data = res.json()
photos_list = {}
print('Загрузка имени и url в словарь:')
for photo in tqdm(data['response']['items']):
    time.sleep(0.3)
    if str(photo['likes']['count']) in photos_list:
        photos_list[str(photo['likes']['count']) + '.' + str(photo['date'])] = photo['sizes'][-1]['url']
    else:
        photos_list[str(photo['likes']['count'])] = photo['sizes'][-1]['url']


folder_name = str(input('Введите имя папки: '))

create_folder(folder_name)

print('Загрузка файлов на Я.Диск:')
index = 0
limit = 5
for el in tqdm(photos_list):
    time.sleep(0.3)
    if index == limit:
        break
    else:
        params = {
        'path': f'{folder_name}/{el}.jpg',
        'url': f'{photos_list[el]}'
        }
        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload/'
        r = requests.post(url=url, params=params, headers=get_headers_ya())
        index += 1

time.sleep(3)
print('Загрузка имени и размера объекта в json файл:')
params = {
        'path': f'{folder_name}/',
}
url = 'https://cloud-api.yandex.net/v1/disk/resources'
r = requests.get(url=url, params=params, headers=get_headers_ya())
req = r.json()
json_list = []
for el in tqdm(req['_embedded']['items']):
    time.sleep(0.3)
    json_dict = {}
    json_dict['file_name'] = str(el['name'].strip())
    json_dict['size'] = el['size']
    json_list.append(json_dict)
with open("new_file.json", "w", encoding="utf-8") as file:
    json.dump(json_list, file)