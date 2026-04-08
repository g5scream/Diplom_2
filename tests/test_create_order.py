import allure
from constants.api_constants import StatusCode, TextResponse
from helpers.user_api import *
from helpers.order_api import create_order, get_random_ingredients


@allure.suite('Создание заказа')
class TestOrderCreate:

    @allure.feature("Создание заказа")
    @allure.title("Создание заказа с авторизацией и ингредиентами")
    def test_create_order_with_auth_and_ingredients(self, create_user, ingredient_ids):
        order_ingredients = [ingredient_ids[0], ingredient_ids[1], ingredient_ids[2]]

        with allure.step("Попытка создания заказа с авторизацией"):
            response = create_order(
                create_user["accessToken"],
                order_ingredients
            )
            allure.attach(
                body=response.text,
                name="Ответ сервера при создании заказа",
                attachment_type=allure.attachment_type.TEXT
            )

        response_data = response.json()
        assert (
            response.status_code == StatusCode.HTTP_200_OK and
            response_data.get("success") is True and
            response_data["order"]["owner"]["name"] == create_user["user"]["name"]
        )
    
    @allure.feature("Создание заказа")
    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth(self, ingredient_ids):
        with allure.step("Попытка создания заказа без токена авторизации"):
            response = create_order(None, [ingredient_ids[1], ingredient_ids[2]])
            allure.attach(
                    body=response.text,
                    name="Ответ сервера при создании заказа без токена",
                    attachment_type=allure.attachment_type.TEXT
                )
        
        response_data = response.json()
        with allure.step("Проверяем ответ сервера"):
            assert response.status_code == StatusCode.HTTP_200_OK and (
                response_data.get("success") is True 
            )

    @allure.feature("Создание заказа")
    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self, create_user):
        with allure.step("Попытка создания заказа без ингредиентов"):
            response = create_order(create_user["accessToken"], [])
            allure.attach(
                body=response.text,
                name="Ответ сервера при создании заказа без ингредиентов",
                attachment_type=allure.attachment_type.TEXT
            )

        response_data = response.json()
        assert (
            response.status_code == StatusCode.BAD_REQUEST and
            response_data.get("success") is False and
            response_data.get("message") == TextResponse.MISSING_INGREDIENTS
        )

    @allure.feature("Создание заказа")
    @allure.title("Создание заказа с неверным хэшем ингредиентов")
    def test_create_order_with_invalid_hash(self, create_user) -> None:
        invalid_ingredient = get_random_ingredients(1)[0] + '1'
        with allure.step("Попытка создания заказа с неверным хэшем ингредиента"):
            response = create_order(
                create_user["accessToken"],
                [invalid_ingredient]
            )
            allure.attach(
                body=response.text,
                name="Ответ сервера при создании заказа с неверным хэшем",
                attachment_type=allure.attachment_type.TEXT
            )

        status_code = response.status_code
        assert status_code == 500

