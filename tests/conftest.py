from collections import namedtuple
from datetime import datetime

import pytest
import structlog
from restclient.configuration import Configuration as DmApiConfiguration
from restclient.configuration import Configuration as MailHogConfiguration
from services.api_mailhog import MailhogApi
from services.dm_api_account import DmApiAccount
from helpers.account_helper import AccountHelper
from pathlib import Path
from vyper import v

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, ensure_ascii=True, sort_keys=True)
    ]
)

options=(
    'service.dm_api_account',
    'service.mailhog',
    'user.login',
    'user.password',
)

@pytest.fixture(scope="session", autouse=True)
def set_config(request):
    config = Path(__file__).joinpath("../../").joinpath("config")
    config_name = request.config.getoption("--env")
    v.set_config_name(config_name)
    v.add_config_path(config)
    v.read_in_config()
    for option in options:
        v.set(f"{option}", request.config.getoption(f"--{option}"))

def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="stg", help="run stg")
    for option in options:
        parser.addoption(f"--{option}", action="store", default=None)

@pytest.fixture(scope="session")
def mailhog_api():
    mailhog_configuration = MailHogConfiguration(host=v.get("service.mailhog"))
    mailhog_client = MailhogApi(configuration=mailhog_configuration)
    return mailhog_client

@pytest.fixture()
def account_api():
    dm_api_configuration = DmApiConfiguration(host=v.get("service.dm_api_account"), disable_log=False)
    account_client = DmApiAccount(configuration=dm_api_configuration)
    return account_client

@pytest.fixture
def account_helper(account_api, mailhog_api):
    account_helper = AccountHelper(dm_account_api=account_api, mailhog=mailhog_api)
    return account_helper

@pytest.fixture
def auth_account_helper(mailhog_api, account_api):
    account_helper = AccountHelper(dm_account_api=account_api, mailhog=mailhog_api)
    account_helper.auth_client(login=v.get("user.login"), password=v.get("user.password"))
    return account_helper

# @pytest.fixture
# def authenticated_user(mailhog_api, account_api, prepare_user):
#     account_helper = AccountHelper(dm_account_api=account_api, mailhog=mailhog_api)
#     account_helper.auth_client(login=prepare_user.login, password=prepare_user.password)
#     return {
#         'account_helper': account_helper,
#         'user_data': prepare_user
#     }

@pytest.fixture
def prepare_user():
    now = datetime.now()
    data = now.strftime("%Y_%m_%dT%H_%M_%S")
    login = f'yantik_{data}'
    password = v.get("user.password")
    email = f'{login}@google.com'
    User = namedtuple("User", ["login", "password", "email"])
    user = User(login=login, password=password, email=email)
    return user
