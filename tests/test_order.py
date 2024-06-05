import allure
import pytest
from helpers import ApiOrder, ApiUser


class TestOrderCreate:
    @allure.title('создание заказа без авторизации, с ингредиентами')
    def test_create_order_success(self):
        ingredients = ApiOrder.get_random_ingredients()
        response = ApiOrder.create_order(ingredients)

        assert response.status_code == 200 and response.json()['success'] is True, \
            f'status code = {response.status_code} and success = {response.json()['success']}'

    @allure.title('создание заказа без авторизации, без ингредиентов')
    def test_create_order_empty_ingredients_error_creation(self):
        ingredients = []
        response = ApiOrder.create_order(ingredients)

        assert response.status_code == 400 and response.json()['success'] is False, \
            f'status code = {response.status_code} and success = {response.json()['success']}'

    @allure.title('создание заказа с авторизацией, с ингредиентами')
    def test_create_order_authorization_user_success(self, random_user):
        response = ApiUser.registration_user(random_user['email'], random_user['password'], random_user['name'])
        token = response.json()['accessToken']
        ingredients = ApiOrder.get_random_ingredients()

        response = ApiOrder.create_order_authorization_user(ingredients, token)
        assert response.status_code == 200 and response.json()['order']['owner']['name'] == random_user['name'], \
            f'status code = {response.status_code} and Owner name = {response.json()['order']['owner']['name']}'

    @allure.title('создание заказа без авторизации, с неверным хэшом ингредиентов')
    @pytest.mark.parametrize(
        'ingredients',
        [
            ['bed_hash1', 'bed_hash2'],
            ['', '  ']
        ]
    )
    def test_create_order_incorrect_ingredient_error_creation(self, ingredients):
        response = ApiOrder.create_order(ingredients)

        assert response.status_code == 500


class TestOrderReceiving:
    @allure.title('получение заказов авторизованного пользователя')
    def test_get_order_authorization_user_success(self, get_random_user_token):
        ingredients = ApiOrder.get_random_ingredients()
        ApiOrder.create_order_authorization_user(ingredients, get_random_user_token)

        response = ApiOrder.get_orders_owner(get_random_user_token)
        assert response.status_code == 200 and response.json()['success'] is True, \
            f'status code = {response.status_code} and success = {response.json()['success']}'

    @allure.title('получение заказов неавторизованного пользователя')
    def test_get_order_unauthorized_error_response(self):
        token = 'incorrect_token'

        response = ApiOrder.get_orders_owner(token)
        assert response.status_code == 401 and response.json()['success'] is False, \
            f'status code = {response.status_code} and success = {response.json()['success']}'