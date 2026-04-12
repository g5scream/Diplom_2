import pytest
import allure
from constants.api_constants import StatusCode, TextResponse
from helpers.user_api import register_user, delete_user
from helpers.data import generate_user


@allure.suite('Регистрация')
class TestUserCreate:

    @allure.feature("Регистрация пользователей")
    @allure.title("Создать уникального пользователя")
    def test_register_unique_user(self):
        user_data = generate_user(is_random=True) # Генерация данных для нового пользователя
        with allure.step("Отправка запроса на регистрацию пользователя"): # логирование с этапа запроса
            response = register_user(
                email=user_data["email"],
                password=user_data["password"],
                name=user_data["name"]
            )

            allure.attach(
                body=response.text,
                name="Ответ сервера при регистрации",
                attachment_type=allure.attachment_type.TEXT
            )
        response_data = response.json()

        with allure.step("Проверка данных созданного пользователя"):
            allure.attach(
                body=str(response_data),
                name="Данные созданного пользователя",
                attachment_type=allure.attachment_type.TEXT
            )

            assert (
                response_data.get("success") is True and
                "accessToken" in response_data and
                "refreshToken" in response_data
            )

        with allure.step("Удаление созданного тестового пользователя"):
            if "accessToken" in response_data:
                delete_response = delete_user(response_data["accessToken"])
                allure.attach(
                    body=delete_response.text,
                    name="Ответ сервера при удалении",
                    attachment_type=allure.attachment_type.TEXT
                )

    @allure.feature("Регистрация пользователей")
    @allure.title("Проверить повторную регистрацию существующего пользователя")
    def test_existing_user_registration(self, clean_user_after_test):
        created_user = clean_user_after_test
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
