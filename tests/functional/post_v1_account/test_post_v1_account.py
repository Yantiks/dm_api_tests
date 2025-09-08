import allure
import pytest
import structlog
from checkers.http_checkers import check_status_code_http

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, ensure_ascii=True, sort_keys=True)
    ]
)


@allure.suite("Тесты на проверку метода POST v1/account")
@allure.sub_suite("Позитивный и негативный тесты POST v1/account")
class TestsPostV1Account:

    @allure.title("Проверка регистрации нового пользователя")
    def test_account_creation(self, account_helper, prepare_user):
        # регистрация нового пользователя
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email
        account_helper.create_user(login=login, password=password, email=email)

    @allure.title("Проверка регистрации нового пользователя с невалидными данными")
    @pytest.mark.parametrize(
        "login, email, password, expected_status_code, error_message",
        [
            # 1. Короткий пароль
            ("validlogin21", "user19@example.com", "123", 400, "Validation failed"),

            # 2. Невалидный email
            ("validlogin18", "invalidemail.com", "validPass123", 400, "Validation failed"),

            # 3. Невалидный логин
            ("a", "user20@example.com", "validPass123", 400, "Validation failed"),
        ]
    )
    def test_post_v1_account_negative(self, account_helper, login, email, password, expected_status_code, error_message):
        login = login
        password = password
        email = email
        with check_status_code_http(expected_status_code, error_message):
            account_helper.create_user(login=login, password=password, email=email)