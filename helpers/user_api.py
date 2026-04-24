import requests
from constants.api_constants import *
from constants.endpoints import *
from helpers.auth_helpers import _get_auth_headers


def register_user(email, password, name):
    payload = {"email": email, "password": password, "name": name}
    return requests.post(Endpoints.REGISTER, json=payload)

def login_user(email, password):
    payload = {"email": email, "password": password}
    return requests.post(Endpoints.LOGIN, json=payload)

def delete_user(access_token):
    headers = _get_auth_headers(access_token)
    return requests.delete(Endpoints.USER, headers=headers)