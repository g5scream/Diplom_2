import requests
import random
from constants.api_constants import *
from constants.endpoints import *
from helpers.auth_helpers import _get_auth_headers  # Общий хелпер


ingredients = {
    '61c0c5a71d1f82001bdaaa6d': 'Флюоресцентная булка R2-D3',
    '61c0c5a71d1f82001bdaaa6f': 'Мясо бессмертных моллюсков Protostomia',
    '61c0c5a71d1f82001bdaaa70': 'Говяжий метеорит (отбивная)',
    '61c0c5a71d1f82001bdaaa71': 'Биокотлета из марсианской Магнолии',
    '61c0c5a71d1f82001bdaaa72': 'Соус Spicy-X',
    '61c0c5a71d1f82001bdaaa6e': 'Филе Люминесцентного тетраодонтимформа',
    '61c0c5a71d1f82001bdaaa73': 'Соус фирменный Space Sauce',
    '61c0c5a71d1f82001bdaaa74': 'Соус традиционный галактический',
    '61c0c5a71d1f82001bdaaa6c': 'Краторная булка N-200i',
    '61c0c5a71d1f82001bdaaa75': 'Соус с шипами Антарианского плоскоходца',
    '61c0c5a71d1f82001bdaaa76': 'Хрустящие минеральные кольца',
    '61c0c5a71d1f82001bdaaa77': 'Плоды Фалленианского дерева',
    '61c0c5a71d1f82001bdaaa78': 'Кристаллы марсианских альфа-сахаридов',
    '61c0c5a71d1f82001bdaaa79': 'Мини-салат Экзо-Плантаго',
    '61c0c5a71d1f82001bdaaa7a': 'Сыр с астероидной плесенью',
}

def get_ingredient_ids():
    response = requests.get(Endpoints.INGREDIENTS)
    response.raise_for_status()
    return [item["_id"] for item in response.json()["data"]]

def create_order(access_token, ingredients):
    headers = _get_auth_headers(access_token)
    payload = {"ingredients": ingredients}
    return requests.post(Endpoints.CREATE_ORDER, headers=headers, json=payload)

def get_random_ingredients(ingredients_count: int = 2) -> list[str]:
    return random.choices(list(ingredients.keys()), k=ingredients_count)