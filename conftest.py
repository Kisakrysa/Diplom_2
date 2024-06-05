import pytest
from helpers import ApiUser


@pytest.fixture(scope='function')
def random_user():
    payload = ApiUser.create_random_user()

    yield payload

    response = ApiUser.login_user(email=payload['email'], password=payload['password'])
    token = response.json()['accessToken']
    ApiUser.delete_user(token)


@pytest.fixture(scope='function')
def get_random_user_token():
    payload = ApiUser.create_random_user()
    response = ApiUser.registration_user(payload['email'], payload['password'], payload['name'])
    token = response.json()['accessToken']

    yield token

    ApiUser.delete_user(token)