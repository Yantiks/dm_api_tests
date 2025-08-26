import time
from json import loads, JSONDecodeError
from retrying import retry

from services.dm_api_account import DmApiAccount
from services.api_mailhog import MailhogApi

def retrier(func):
    def wrapper(*args, **kwargs):
        token = None
        count = 0
        while token is None:
            token = func(*args, **kwargs)
            count+=1
            if count==5:
                raise AssertionError("Превышено количество попыток получения токена")
            if token:
                return token
            time.sleep(1)

    return wrapper


class AccountHelper:
    def __init__(self, dm_account_api: DmApiAccount, mailhog: MailhogApi = None):
        self.dm_account_api = dm_account_api
        self.mailhog = mailhog

    def create_user(self, login:str, password:str, email:str):
        json_data = {
            'login': login,
            'email': email,
            'password': password,
        }
        response_login = self.dm_account_api.account_api.post_v1_account(json_data=json_data)
        assert response_login.status_code == 201, f"Пользователь не был создан, код ошибки: {response_login.status_code}"
        return response_login

    def register_new_user(self, login:str, password:str, email:str):
        response_login = self.create_user(login, password, email)
        activate_token = self.get_and_activate_token(login=login)
        return activate_token

    def get_and_activate_token(self, login:str):
        # response_mail = self.mailhog.mailhog_api.get_api_v2_messages()
        # assert response_mail.status_code == 200, "Письма не были получены"
        token = self.get_activation_token(login=login)
        assert token is not None, f"Токен для пользователя {login} не был получен"
        activate_token = self.dm_account_api.account_api.put_v1_account_token(token=token)
        assert activate_token.status_code == 200, "Токен не был активирован"

        return activate_token

    def user_login(self, login:str, password:str, rememberMe:bool=True):
        json_data = {
            'login': login,
            'password': password,
            'rememberMe': True,
        }
        response = self.dm_account_api.login_api.post_v1_account_login(json_data=json_data)
        # assert response.status_code == 403, f"Пользователь был авторизован, код ответа: {response.status_code}"

        return response

    def change_email(self, login:str, password:str, email:str):
        json_data_new = {
            'login': login,
            'password': password,
            'email': email,
        }

        response = self.dm_account_api.account_api.put_v1_account_email(json_data=json_data_new)
        assert response.status_code == 200, f"Почта для пользователя {login} не была изменена"
        return response

    @retrier
    def get_activation_token(self, login):
        token = None
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        for item in response.json()['items']:
            # user_data = loads(item['Content']['Body'])
            try:
                user_data = loads(item['Content']['Body'])
            except (KeyError, JSONDecodeError):
                continue
            user_login = user_data['Login']
            if user_login == login:
                token = user_data['ConfirmationLinkUrl'].split('/')[-1]
        return token