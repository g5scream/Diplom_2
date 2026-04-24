import pytest
import allure
from helpers.data import generate_user
from helpers import user_api
from helpers.order_api import get_ingredient_ids


@pytest.fixture # генерация данных пользователя
def create_user_data():
    user_data = generate_user(is_random=True)
    with allure.step("Генерация тестовых данных пользователя"):
        allure.attach(
            body=str(user_data),
            name="Сгенерированные данные пользователя",
            attachment_type=allure.attachment_type.TEXT
        )
    return user_data

@pytest.fixture # регистрация пользователя через API
def registered_user(create_user_data):
    user_data = create_user_data
    with allure.step("Создание тестового пользователя через API"):
        response = user_api.register_user(
            email=user_data["email"],
            password=user_data["password"],
            name=user_data["name"]
        )
        allure.attach(
            body=response.text,
            name="Ответ сервера при регистрации",
            attachment_type=allure.attachment_type.TEXT
        )
        created_user = response.json()
        created_user["password"] = user_data["password"]
    return created_user

@pytest.fixture # удаления пользователя после теста
def clean_user_after_test(registered_user):
    created_user = registered_user
    token = created_user.get("accessToken")
    yield created_user
    if token:
        with allure.step("Удаление тестового пользователя"):
            delete_response = user_api.delete_user(token)
            allure.attach(
                body=delete_response.text,
                name="Ответ сервера при удалении",
                attachment_type=allure.attachment_type.TEXT
            )

@pytest.fixture(scope="module")
def ingredient_ids():
    return get_ingredient_ids()
