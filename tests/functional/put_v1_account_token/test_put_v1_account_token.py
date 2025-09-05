import allure
import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, ensure_ascii=True, sort_keys=True)
    ]
)

@allure.title("Проверка активации токена")
def test_put_account_token(account_helper, prepare_user):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    # регистрация нового пользователя
    # получение токена с почты
    # активация токена
    account_helper.register_new_user(login=login, password=password, email=email)