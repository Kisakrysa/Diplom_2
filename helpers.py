import allure
import string
import requests
import data
from random import choice


class ApiOrder:
    @staticmethod
    @allure.step('cоздание заказа')
    def create_order(ingredients: list):
        payload = {"ingredients": ingredients}

        response = requests.post(data.Urls.CREATE_ORDER, data=payload)
        return response

    @staticmethod
    @allure.step('создание заказа с авторизацией')
    def create_order_authorization_user(ingredients: list, token):
        payload = {"ingredients": ingredients}
        header = {"Authorization": token}

        response = requests.post(data.Urls.CREATE_ORDER, data=payload, headers=header)
        return response

    @staticmethod
    @allure.step('вывод списка ингридиентов')
    def get_random_ingredients():
        response = requests.get(data.Urls.GET_INGREDIENTS)
        ingredients = []

        for i in response.json()['data']:
            ingredients.append(i['_id'])

        random_ingredients = []
        for i in range(3):
            random_ingredients.append(choice(ingredients))

        return random_ingredients

    @staticmethod
    @allure.step('вывод заказов пользователя')
    def get_orders_owner(token: str):
        header = {"Authorization": token}

        response = requests.get(data.Urls.CREATE_ORDER, headers=header)
        return response


class ApiUser:
    @staticmethod
    @allure.step('рандомный пользователь')
    def create_random_user():
        def generate_random_string(length):
            letters = string.ascii_lowercase
            random_string = ''.join(choice(letters) for i in range(length))
            return random_string

        payload = {
            "email": generate_random_string(6) + '@yandex.ru',
            "password": generate_random_string(6),
            "name": generate_random_string(6)
        }

        return payload

    @staticmethod
    @allure.step('регистрация')
    def registration_user(email: str, password: str, name: str):
        payload = {
            "email": email,
            "password": password,
            "name": name
        }

        response = requests.post(data.Urls.USER_REGISTER, data=payload)
        return response

    @staticmethod
    @allure.step('логин на сайт')
    def login_user(email: str, password: str):
        payload = {
            "email": email,
            "password": password
        }

        response = requests.post(data.Urls.USER_LOGIN, data=payload)
        return response

    @staticmethod
    @allure.step('удаление аккаунта')
    def delete_user(token: str):
        headers = {"Authorization": token}

        response = requests.delete(data.Urls.USER, headers=headers)
        return response

    @staticmethod
    @allure.step('релактирование данных пользователя')
    def modify_user(email: str, password: str, token: str):
        payload = {
            "email": email,
            "password": password
        }
        header = {"Authorization": token}

        response = requests.patch(data.Urls.USER, data=payload, headers=header)
        return response
