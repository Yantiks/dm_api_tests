
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

def test_login_with_changed_email():
    mailhog_configuration = MailHogConfiguration(host='http://5.63.153.31:5025')
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)

    account = DmApiAccount(configuration=dm_api_configuration)
    mailhog = MailhogApi(configuration=mailhog_configuration)

    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog)

    # регистрация нового пользователя
    login = 'yantik_test112'
    password = "12345abcdi"
    email = f'{login}@google.com'
    account_helper.create_user(login=login, password=password, email=email)

    # изменение почты пользователя
    account_helper.change_email(login=login, password=password, email=email)

    # попытка авторизации со старым токеном
    account_helper.user_login(login=login, password=password)

    # получение нового токена с почты
    # активация нового токена
    account_helper.get_and_activate_token(login=login)

    # логин с новым токеном
    account_helper.user_login(login=login, password=password)
