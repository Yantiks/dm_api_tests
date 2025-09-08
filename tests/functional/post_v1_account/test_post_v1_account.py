import pytest
import structlog
from checkers.http_checkers import check_status_code_http

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, ensure_ascii=True, sort_keys=True)
    ]
)


def test_account_creation(account_helper, prepare_user):
    # регистрация нового пользователя
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    account_helper.create_user(login=login, password=password, email=email)



@pytest.mark.parametrize(
    "login, email, password, expected_status_code, error_message",
    [
        # 1. Короткий пароль
        ("validlogin8", "user8@example.com", "123", 400, "Validation failed"),

        # 2. Невалидный email
        ("validlogin9", "invalidemail.com", "validPass123", 400, "Validation failed"),

        # 3. Невалидный логин
        ("a", "user9@example.com", "validPass123", 400, "Validation failed"),
    ]
)
def test_post_v1_account_negative(account_helper, login, email, password, expected_status_code, error_message):
    login = login
    password = password
    email = email
    with check_status_code_http(expected_status_code, error_message):
        account_helper.create_user(login=login, password=password, email=email)