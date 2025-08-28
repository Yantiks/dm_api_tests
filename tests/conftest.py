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
def auth_account_helper(mailhog_api):
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)
    account = DmApiAccount(configuration=dm_api_configuration)
    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog_api)
    account_helper.auth_client(login="yantik_test200", password="12345abcdi")
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
