import allure

from checkers.post_v1_account_login import PostV1AccountLogin


@allure.title("Проверка авторизации пользователя")
def test_login_account(account_helper, prepare_user):
    # регистрация нового пользователя
    # получение токена с почты
    # активация токена
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    account_helper.register_new_user(login=login, password=password, email=email)
    # авторизация
    response = account_helper.user_login(login=login, password=password, validate_response=True)
    PostV1AccountLogin.check_response_values(response)