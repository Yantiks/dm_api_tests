import allure


@allure.title("Проверка смены пароля пользователя")
def test_put_v1_account_password(account_helper, prepare_user):
    # регистрация нового пользователя
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    new_password = "new" + password

    account_helper.register_new_user(login=login, password=password, email=email)
    account_helper.auth_client(login=login, password=password)

    reset_token = account_helper.reset_password(login=login, email=email)
    account_helper.change_password(login=login, old_password=password, new_password=new_password, token=reset_token)

    account_helper.user_login(login=login, password=new_password)
