from account_api import AccountApi
from login_api import LoginApi
from mail_api import MailApi


def test_login_with_token():
    account_api = AccountApi(host='http://5.63.153.31:5051')
    login_api = LoginApi(host='http://5.63.153.31:5051')
    mail_api = MailApi(host='http://5.63.153.31:5025')

    login = 'yantik_test1'
    password = "12345"
    email = f'{login}@google.com'
    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }
    response_login = account_api.post_account(json_data)
    print(response_login.status_code)
    assert response_login.status_code == 201, f"Пользователь не был создан, код ошибки: {response_login.json()}"

    response_mail = mail_api.get_messages()
    print(response_mail)
# регистрация
# получение токена
# активация токена
# заходим
# меняем имейл
# попытка входа, 403
# получение токена с почты
# активация нового токена
# логин