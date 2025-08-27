
def test_login_account(account_helper, prepare_user):
    # регистрация нового пользователя
    # получение токена с почты
    # активация токена
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    account_helper.register_new_user(login=login, password=password, email=email)
    # авторизация
    account_helper.user_login(login=login, password=password)