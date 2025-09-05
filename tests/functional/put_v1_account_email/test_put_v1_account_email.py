import allure
import structlog

from checkers.http_checkers import check_status_code_http

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, ensure_ascii=True, sort_keys=True)
    ]
)

@allure.title("Проверка смены имейла пользователя")
def test_login_with_changed_email(account_helper, prepare_user):
    # регистрация нового пользователя
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    new_email = "new" + email
    account_helper.create_user(login=login, password=password, email=email)

    # изменение почты пользователя
    account_helper.change_email(login=login, password=password, email=new_email)

    # попытка авторизации со старым токеном
    with check_status_code_http(403, 'User is inactive. Address the technical support for more details'):
        account_helper.user_login(login=login, password=password)

    # получение нового токена с почты
    # активация нового токена
    account_helper.get_and_activate_token(login=login)

    # логин с новым токеном
    account_helper.user_login(login=login, password=password)
