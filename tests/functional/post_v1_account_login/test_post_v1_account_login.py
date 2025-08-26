
import structlog
from restclient.configuration import Configuration as DmApiConfiguration
from restclient.configuration import Configuration as MailHogConfiguration
from services.api_mailhog import MailhogApi
from services.dm_api_account import DmApiAccount
from helpers.account_helper import AccountHelper

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

    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog)

    # регистрация нового пользователя
    # получение токена с почты
    # активация токена
    login = 'yantik_test120'
    password = "12345abcdi"
    email = f'{login}@google.com'
    account_helper.register_new_user(login=login, password=password, email=email)

    # авторизация
    account_helper.user_login(login=login, password=password)