
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

def test_login_with_changed_email():
    mailhog_configuration = MailHogConfiguration(host='http://5.63.153.31:5025')
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)

    account = DmApiAccount(configuration=dm_api_configuration)
    mailhog = MailhogApi(configuration=mailhog_configuration)

    # регистрация нового пользователя
    login = 'yantik_test127'
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

    # изменение почты пользователя
    json_data_new = {
        'login': login,
        'password': password,
        'email': "new" + email,
    }

    change_email = account.account_api.put_v1_account_email(json_data=json_data_new)
    assert change_email.status_code == 200, f"Почта для пользователя {login} не была изменена"

    # попытка авторизации со старым токеном
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }
    try_enter = account.login_api.post_v1_account_login(json_data=json_data)
    assert try_enter.status_code == 403, f"Пользователь был авторизован, код ответа: {try_enter.status_code}"

    # получение нового токена с почты
    response_mail = mailhog.mailhog_api.get_api_v2_messages()
    assert response_mail.status_code == 200, "Письма не были получены"
    token = mailhog.mailhog_api.get_activation_token(login=login, response=response_mail)
    assert token is not None, f"Токен для пользователя {login} не был получен"

    # активация нового токена
    activate_token = account.account_api.put_v1_account_token(token=token)
    assert activate_token.status_code == 200, "Токен не был активирован"

    # логин с новым токеном
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }
    try_enter = account.login_api.post_v1_account_login(json_data=json_data)
    assert try_enter.status_code == 200, f"Пользователь не был авторизован, код ошибки: {try_enter.status_code}"
