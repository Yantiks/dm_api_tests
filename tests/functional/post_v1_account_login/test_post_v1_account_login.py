from collections import namedtuple
from datetime import datetime

import pytest
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

@pytest.fixture
def mailhog_api():
    mailhog_configuration = MailHogConfiguration(host='http://5.63.153.31:5025')
    mailhog_client = MailhogApi(configuration=mailhog_configuration)
    return mailhog_client

@pytest.fixture
def account_api():
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)
    account_client = DmApiAccount(configuration=dm_api_configuration)
    return account_client

@pytest.fixture
def account_helper(account_api, mailhog_api):
    account_helper = AccountHelper(dm_account_api=account_api, mailhog=mailhog_api)
    return account_helper

@pytest.fixture
def prepare_user():
    now = datetime.now()
    data = now.strftime("%Y_%m_%dT%H_%M_%S")
    login = f'yantik_{data}'
    password = "12345abcdi"
    email = f'{login}@google.com'
    User = namedtuple("User", ["login", "password", "email"])
    user = User(login=login, password=password, email=email)
    return user


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