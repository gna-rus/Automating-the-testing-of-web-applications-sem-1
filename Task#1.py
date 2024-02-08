import functools
import requests
import pytest
import yaml

with open('config.yaml') as f:
    # читаем документ YAML
    data = yaml.safe_load(f)


def decorator_loggin(func):
    @functools.wraps(func)
    def wrapper():
        response_post = requests.post(data['url_login'], data={'username': data['username'], 'password': data['passwd']})
        return func(response_post.json()['token'])
    return wrapper

@decorator_loggin
def get_post(token):
    # возрвращае состояние поста
    resource = requests.get(data['url_post'], headers={"X-Auth-Token": token}, params={"owner": "notMe"})
    return resource.json()


def list_of_id():
    result = get_post()
    lst = []
    for item in result['data']:
        print(item)


print(get_post())
print(list_of_id())
