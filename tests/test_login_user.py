import allure
from constants.api_constants import StatusCode, TextResponse
from helpers.user_api import login_user


@allure.suite('Авторизация')
class TestLoginUser:

    @allure.feature("Авторизация пользователей")
    @allure.title("Успешная авторизация зарегистрированного пользователя")
    def test_successful_login(self, clean_user_after_test):
        user_email = clean_user_after_test["user"]["email"]
        user_password = clean_user_after_test["password"]

        with allure.step("Попытка успешного входа"):
            login_response = login_user(user_email, user_password)
            
            allure.attach(
                body=login_response.text,
                name="Ответ сервера при успешной авторизации",
                attachment_type=allure.attachment_type.TEXT
            )

            assert (
                login_response.status_code == StatusCode.HTTP_200_OK and
                login_response.json().get("success") is True
            )


    @allure.feature("Авторизация пользователей")
    @allure.title("Неуспешная авторизация с неверными учётными данными")
    def test_unsuccessful_login(self):
        wrong_user = {
            "email": "wrong_email@example.com",
            "password": "wrong_password"
        }

        with allure.step("Попытка входа с неверным email и паролем"):
            response = login_user(wrong_user["email"], wrong_user["password"])

            allure.attach(
                body=response.text,
                name="Ответ сервера при неудачной авторизации",
                attachment_type=allure.attachment_type.TEXT
            )

            assert (
                response.status_code == StatusCode.UNAUTH and
                response.json().get("message") == TextResponse.INVALID_CREDENTIALS
            )
            