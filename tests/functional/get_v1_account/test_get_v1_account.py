from datetime import datetime

import allure
from assertpy import soft_assertions, assert_that

from checkers.get_v1_account import GetV1Account
from checkers.http_checkers import check_status_code_http
from dm_api_account.models.user_details_envelope import UserRole


@allure.suite("Тесты на проверку метода GET v1/account")
@allure.sub_suite("Позитивный и негативный тесты GET v1/account")
class TestsGetV1Account:

    @allure.title("Проверка получения данных об авторизованном пользователе")
    def test_get_v1_account(self, auth_account_helper):
        with check_status_code_http():
            response = auth_account_helper.get_client()
            GetV1Account.check_response_values(response)

    @allure.title("Проверка получения данных о неавторизованном пользователе")
    def test_get_v1_account_no_auth(self, account_helper):
        with check_status_code_http(401, 'User must be authenticated'):
            account_helper.get_client()

    @allure.title("Проверка получения данных об авторизованном пользователе")
    # использование soft-assertions
    def test_get_v1_account(self, auth_account_helper):
            response = auth_account_helper.get_client()
            with soft_assertions():
                assert_that(response.resource.login).is_equal_to('yantik_test200')
                print("Прошла проверка типа поля логин")
                assert_that(response.resource.online).is_instance_of(datetime)
                print("Прошла проверка типа поля online")
                assert_that(response.resource.roles).contains(UserRole.GUEST, UserRole.PLAYER)
                print("Прошла проверка ролей пользователя")
