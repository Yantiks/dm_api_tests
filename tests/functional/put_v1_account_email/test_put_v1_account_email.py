from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mail_api import MailApi


def test_login_with_changed_email():
    account_api = AccountApi(host='http://5.63.153.31:5051')
    login_api = LoginApi(host='http://5.63.153.31:5051')
    mail_api = MailApi(host='http://5.63.153.31:5025')

    # регистрация нового пользователя
    login = 'yantik_test40'
    password = "12345abcdi"
    email = f'{login}@google.com'
    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }
    response_login = account_api.post_v1_account(json_data)
    assert response_login.status_code == 201, f"Пользователь не был создан, код ошибки: {response_login.status_code}"

    # получение токена с почты
    response_mail = mail_api.get_api_v2_messages()
    assert response_mail.status_code == 200, "Письма не были получены"
    token = mail_api.get_activation_token(login=login, response=response_mail)
    print(f'token: {token}')
    print(response_mail.status_code)
    assert token is not None, f"Токен для пользователя {login} не был получен"

    # активация токена
    activate_token = account_api.put_v1_account_token(token=token)
    print(f'activate_token: {activate_token.json()}')
    print(activate_token.status_code)
    assert activate_token.status_code == 200, "Токен не был активирован"

    # изменение почты пользователя
    json_data_new = {
        'login': login,
        'password': password,
        'email': "new" + email,
    }

    change_email = account_api.put_v1_account_email(json_data=json_data_new)
    print(f'change_email: {change_email.json()}')
    print(change_email.status_code)
    assert change_email.status_code == 200, f"Почта для пользователя {login} не была изменена"

    # попытка авторизации со старым токеном
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }
    try_enter = login_api.post_v1_account_login(json_data=json_data)
    print(try_enter.status_code)
    assert try_enter.status_code == 403, f"Пользователь был авторизован, код ответа: {try_enter.status_code}"

    # получение нового токена с почты
    response_mail = mail_api.get_api_v2_messages()
    assert response_mail.status_code == 200, "Письма не были получены"
    token = mail_api.get_activation_token(login=login, response=response_mail)
    print(f'token: {token}')
    print(response_mail.status_code)
    assert token is not None, f"Токен для пользователя {login} не был получен"

    # активация нового токена
    activate_token = account_api.put_v1_account_token(token=token)
    print(f'activate_token: {activate_token.json()}')
    print(activate_token.status_code)
    assert activate_token.status_code == 200, "Токен не был активирован"

    # логин с новым токеном
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }
    try_enter = login_api.post_v1_account_login(json_data=json_data)
    print(try_enter.status_code)
    assert try_enter.status_code == 200, f"Пользователь не был авторизован, код ошибки: {try_enter.status_code}"
