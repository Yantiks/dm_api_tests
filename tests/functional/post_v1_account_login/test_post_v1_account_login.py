
import structlog
from restclient.configuration import Configuration as DmApiConfiguration
from restclient.configuration import Configuration as MailHogConfiguration
from services.api_mailhog import MailhogApi
from services.dm_api_account import DmApiAccount

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, ensure_ascii=True, sort_keys=True)
    ]
)

def test_login_account():
    mailhog_configuration = MailHogConfiguration(host='http://5.63.153.31:5025')
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)

    account = DmApiAccount(configuration=dm_api_configuration)
    mailhog = MailhogApi(configuration=mailhog_configuration)

    # регистрация нового пользователя
    login = 'yantik_test86'
    password = "12345abcdi"
    email = f'{login}@google.com'
    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }
    response_login = account.account_api.post_v1_account(json_data)
    assert response_login.status_code == 201, f"Пользователь не был создан, код ошибки: {response_login.status_code}"

    # получение токена с почты
    response_mail = mailhog.mailhog_api.get_api_v2_messages()
    assert response_mail.status_code == 200, "Письма не были получены"
    token = mailhog.mailhog_api.get_activation_token(login=login, response=response_mail)
    assert token is not None, f"Токен для пользователя {login} не был получен"

    # активация токена
    activate_token = account.account_api.put_v1_account_token(token=token)
    assert activate_token.status_code == 200, "Токен не был активирован"

    # авторизация
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }
    try_login = account.login_api.post_v1_account_login(json_data=json_data)

    assert try_login.status_code == 200, f"Пользователь не был авторизован, код ошибки: {try_login.status_code}"