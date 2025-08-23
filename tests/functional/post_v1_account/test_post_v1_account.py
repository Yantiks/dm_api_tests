from dm_api_account.apis.account_api import AccountApi
import structlog
from restclient.configuration import Configuration as AccountConfiguration

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, ensure_ascii=True, sort_keys=True)
    ]
)

def test_account_creation():
    account_configuration = AccountConfiguration(host='http://5.63.153.31:5051', disable_log=False)
    account_api = AccountApi(account_configuration)

    # регистрация нового пользователя
    login = 'yantik_test80'
    password = "12345abcdi"
    email = f'{login}@google.com'
    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }
    response_login = account_api.post_v1_account(json_data)
    assert response_login.status_code == 201, f"Пользователь не был создан, код ошибки: {response_login.status_code}"