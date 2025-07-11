import requests
import json


def act_get():
    url = 'http://127.0.0.1:8080/giikin/get/test'
    data_json = {"name": "Shi Tou", "password": "123456"}
    res = requests.get(url, params=data_json)
    print(res.text)

def at_post():
    url = 'http://127.0.0.1:8080/giikin/post/test'
    data_json = {"name": "Shi Tou", "password": "123456"}
    res = requests.post(url, data=json.dumps(data_json))
    print(res.text)



if __name__ == '__main__':
    # act_get()
    # at_post()
    ...
