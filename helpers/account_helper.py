import time
from json import loads, JSONDecodeError
from retrying import retry

from dm_api_account.models.change_email import ChangeEmail
from dm_api_account.models.change_password import ChangePassword
from dm_api_account.models.login_credentials import LoginCredentials
from dm_api_account.models.registration import Registration
from dm_api_account.models.reset_password import ResetPassword
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
            time.sleep(3)

    return wrapper


class AccountHelper:
    def __init__(self, dm_account_api: DmApiAccount, mailhog: MailhogApi = None):
        self.dm_account_api = dm_account_api
        self.mailhog = mailhog

    def create_user(self, login:str, password:str, email:str):
        registration = Registration(
            login=login,
            password=password,
            email=email)
        response_login = self.dm_account_api.account_api.post_v1_account(registration=registration)
        # assert response_login.status_code == 201, f"Пользователь не был создан, код ошибки: {response_login.status_code}"
        return response_login

    def register_new_user(self, login:str, password:str, email:str):
        self.create_user(login, password, email)
        activate_token = self.get_and_activate_token(login=login)
        return activate_token

    def get_and_activate_token(self, login:str):
        start_time = time.time()
        token = self.get_token(login=login)
        end_time = time.time()
        assert end_time - start_time < 3, 'Время ожидания активации превышено'
        assert token is not None, f"Токен для пользователя {login} не был получен"
        activate_token = self.dm_account_api.account_api.put_v1_account_token(token=token)
        assert activate_token.status_code == 200, "Токен не был активирован"

        return activate_token

    def user_login(self, login:str, password:str, remember_me:bool=True):
        login_credentials = LoginCredentials(
            login=login,
            password=password,
            remember_me = remember_me
        )
        response = self.dm_account_api.login_api.post_v1_account_login(login_credentials=login_credentials)
        # assert response.status_code == 403, f"Пользователь был авторизован, код ответа: {response.status_code}"
        return response

    def get_auth_token_header(self, response):
        token = {"x-dm-auth-token": response.headers["x-dm-auth-token"]}
        return token

    def change_email(self, login:str, password:str, email:str):
        change_email = ChangeEmail(
            login=login,
            password=password,
            email=email
        )

        response = self.dm_account_api.account_api.put_v1_account_email(change_email=change_email)
        assert response.status_code == 200, f"Почта для пользователя {login} не была изменена"
        return response

    def reset_password(self, login:str, email:str):
        reset_password = ResetPassword(login=login, email=email)
        response = self.dm_account_api.account_api.post_v1_account_password(reset_password=reset_password)
        assert response.status_code == 200, f"Пароль не был сброшен, код ошибки: {response.status_code}"
        token = self.get_token(login=login, token_type="reset")
        assert token is not None, f"Токен для пользователя {login} не был получен"
        return token

    def change_password(self, login:str, old_password:str, new_password:str, token:str):
        change_password = ChangePassword(
            login=login,
            token=token,
            oldpassword=old_password,
            newpassword=new_password,
        )

        response = self.dm_account_api.account_api.put_v1_account_password(change_password=change_password)
        assert response.status_code == 200, f"Пароль для пользователя {login} не был изменён"
        return response

    def auth_client(self, login:str, password:str):
        response = self.user_login(login=login, password=password)
        token = {"x-dm-auth-token": response.headers["x-dm-auth-token"]}
        assert response.headers["x-dm-auth-token"], 'Токен не был получен'
        self.dm_account_api.account_api.set_headers(token)
        self.dm_account_api.login_api.set_headers(token)

    def get_client(self):
        response = self.dm_account_api.account_api.get_v1_account()
        assert response.status_code == 200, f"Данные не были получены"
        return response

    def logout_current_user(self, response):
        token_header = self.get_auth_token_header(response)
        response = self.dm_account_api.login_api.delete_v1_account_login(headers=token_header)
        assert response.status_code == 204, f"Выход не был осуществлён"
        return response

    def logout_all(self):
        response = self.dm_account_api.login_api.delete_v1_account_login_all()
        assert response.status_code == 204, f"Выход не был осуществлён"
        return response

    @retrier
    def get_token(self, login, token_type="activation"):
        token = None
        response = self.mailhog.mailhog_api.get_api_v2_messages()

        for item in response.json()["items"]:
            user_data = loads(item["Content"]["Body"])
            user_login = user_data["Login"]
            activation_token = user_data.get("ConfirmationLinkUrl")
            reset_token = user_data.get("ConfirmationLinkUri")
            if user_login == login and activation_token and token_type == "activation":
                token = activation_token.split("/")[-1]
            elif user_login == login and reset_token and token_type == "reset":
                token = reset_token.split("/")[-1]
        return token