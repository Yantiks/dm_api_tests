
import structlog
from restclient.configuration import Configuration as DmApiConfiguration
from services.dm_api_account import DmApiAccount

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, ensure_ascii=True, sort_keys=True)
    ]
)

def test_account_creation():
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)
    account = DmApiAccount(configuration=dm_api_configuration)

    # регистрация нового пользователя
    login = 'yantik_test87'
    password = "12345abcdi"
    email = f'{login}@google.com'
    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }
    response_login = account.account_api.post_v1_account(json_data)
    assert response_login.status_code == 201, f"Пользователь не был создан, код ошибки: {response_login.status_code}"