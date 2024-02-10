import functools
import json

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


def find_id():
    result = get_post()
    flag = False
    for item in result['data']:
        print(item)
        if 97820 == item['id']:
            flag = True
    return flag
#
# def test_id():
#     assert find_id(), 'Faile Test-id'

@decorator_loggin
def generate_post(token):
    in_post = {"title": "1", "description": "11", "content": "111"} # передаваемые данные
    auth_post = [('username', data['username']), ('password', data['passwd']),( "title", "1"), ("description", "11"), ("content", "111")]
    auth_post1 = [('username', data['username']), ('password', data['passwd'])]
    # передачаа поста (передается токкен регистрации и данные)
    response_post = requests.post(data['url_post'], headers={"X-Auth-Token": token}, data=in_post)
    answer1 = response_post.status_code
    print(answer1)

    return response_post.json()

print(find_id())
print(generate_post())

