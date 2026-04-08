import pytest
import allure
from constants.api_constants import StatusCode, TextResponse
from helpers.user_api import register_user
from helpers.data import generate_user


@allure.suite('Регистрация')
class TestUserCreate:

    @allure.feature("Регистрация пользователей")
    @allure.title("Создать уникального пользователя")
    def test_register_unique_user(self, create_user):
        user_data = create_user
        
        with allure.step("Проверка данных созданного пользователя"):
            allure.attach(
                body=str(user_data),
                name="Данные созданного пользователя",
                attachment_type=allure.attachment_type.TEXT
            )
            
            assert (
                user_data.get("success") is True and
                "accessToken" in user_data and
                "refreshToken" in user_data
            )

    @allure.feature("Регистрация пользователей")
    @allure.title("Проверить повторную регистрацию существующего пользователя")
    def test_existing_user_registration(self, create_user):
        created_user = create_user
        with allure.step("Попытка повторной регистрации существующего пользователя"): # пытаемся зарегистрировать его повторно
            response = register_user(
                created_user["user"]["email"],
                created_user["password"],                         
                created_user["user"]["name"]
            )
            
            allure.attach(
                body=response.text,
                name="Ответ сервера при попытке повторной регистрации",
                attachment_type=allure.attachment_type.TEXT
            )
            
            assert (
                response.status_code == StatusCode.FORBIDDEN and
                response.json().get("message") == TextResponse.USER_EXISTS
            )

    @allure.feature("Регистрация пользователей")
    @allure.title("Создать пользователя и не заполнить одно из обязательных полей")
    @pytest.mark.parametrize("required_field", ["email", "password", "name"])
    def test_registration_with_missing_fields(self, required_field):
        user_data = generate_user()
        del user_data[required_field]
        
        with allure.step(f"Отправка данных без поля '{required_field}'"):
            response = register_user(
                user_data.get("email", ""),
                user_data.get("password", ""),
                user_data.get("name", "")
            )
            
            allure.attach(
                body=response.text,
                name="Ответ сервера при отсутствии обязательных полей",
                attachment_type=allure.attachment_type.TEXT
            )
            
            assert (
                response.status_code == StatusCode.FORBIDDEN and
                response.json().get("message") == TextResponse.MISSING_FIELDS
            )
