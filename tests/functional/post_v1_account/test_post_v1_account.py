
import structlog
from restclient.configuration import Configuration as DmApiConfiguration
from services.dm_api_account import DmApiAccount
from helpers.account_helper import AccountHelper

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, ensure_ascii=True, sort_keys=True)
    ]
)

def test_account_creation():
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)
    account = DmApiAccount(configuration=dm_api_configuration)

    account_helper = AccountHelper(dm_account_api=account)

    # регистрация нового пользователя
    login = 'yantik_test151'
    password = "12345abcdi"
    email = f'{login}@google.com'
    account_helper.create_user(login=login, password=password, email=email)