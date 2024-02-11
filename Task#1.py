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


def find_id(find_id):
    # функция ищет переданный в нее id в посте
    result = get_post()
    flag = False
    for item in result['data']:
        print(item)
        if find_id == item['id']:
            flag = True
    return flag
#


@decorator_loggin
def generate_post(token):
    # функция создающая пост
    in_post = {"title": "test_title", "description": "test_description", "content": "test_content"} # передаваемые данные

    # передачаа поста (передается токкен регистрации и данные)
    response_post = requests.post(data['url_post'], headers={"X-Auth-Token": token}, data=in_post)
    answer_code = response_post.status_code
    return response_post.json(), answer_code

@decorator_loggin
def find_post(token):
    resource = requests.get(data['url_profil'], headers={"X-Auth-Token": token})
    return resource.json()

def test_find_id():
    #Тест на поиск id в ответе
    assert find_id(97954) == True, 'Test of find id - False'


result_test_of_generate = generate_post()

def test_generate_post_code():
    #Тест на определение кода ответа
    assert result_test_of_generate[1] == 200, 'Test code of generate post - False'

def test_generate_post_title():
    # Тест на поиск Title в созданном посте
    assert result_test_of_generate[0]['title'] == 'test_title', 'Test: Title - False'

def test_generate_post_description():
    # Тест на поиск description в созданном посте
    assert result_test_of_generate[0]['description'] == 'test_description', 'Test: Description - False'

def test_generate_post_content():
    # Тест на поиск content в созданном посте
    assert result_test_of_generate[0]['content'] == 'test_content', 'Test: Content - False'