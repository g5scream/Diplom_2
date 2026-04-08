import pytest
import allure
from helpers.data import generate_user
from helpers import user_api
from helpers.order_api import get_ingredient_ids


@pytest.fixture
def create_user():
    user_data = generate_user(is_random=True) # Создание пользователя
    
    with allure.step("Создание тестового пользователя"):
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

    yield created_user

    token = created_user.get("accessToken") # Очистка после теста
    if token:
        with allure.step("Удаление тестового пользователя"):
            delete_response = user_api.delete_user(token)
                
            allure.attach(
                body=delete_response.text,
                name="Ответ сервера при удалении",
                    attachment_type=allure.attachment_type.TEXT
            )

            with allure.step(f"Проверка статуса удаления: {delete_response.status_code}"):
                assert delete_response.status_code == 202


@pytest.fixture(scope="module")
def ingredient_ids():
    return get_ingredient_ids()
