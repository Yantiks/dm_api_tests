import allure
import requests

from dm_api_account.models.login_credentials import LoginCredentials
from dm_api_account.models.user_envelope import UserEnvelope
from restclient.client import RestClient

class LoginApi(RestClient):

    @allure.step("Авторизация пользователя")
    # логин пользователя
    def post_v1_account_login(self, login_credentials:LoginCredentials, validate_response:bool=False):
        """"
        Authenticate via credentials
        :return:
        """
        response = self.post(
            path='/v1/account/login',
            json=login_credentials.model_dump(exclude_none=True, by_alias=True)
        )
        if validate_response:
            return UserEnvelope(**response.json())
        return response

    @allure.step("Логаут текущего пользователя")
    def delete_v1_account_login(self, headers):
        """"
        Logout as current user
        :return:
        """

        response = self.delete(
            path='/v1/account/login',
            headers = headers
        )
        return response

    @allure.step("Логаут со всех устройств")
    def delete_v1_account_login_all(self):
        """"
        Logout from every device
        :return:
        """

        response = self.delete(
            path='/v1/account/login/all'
        )
        return response