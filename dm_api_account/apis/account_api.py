import requests
from restclient.client import RestClient

class AccountApi(RestClient):

    # метод для регистрации пользователя
    def post_v1_account(self, json_data):
        """"
        Register new user
        :param json_data:
        :return:
        """

        response = self.post(
            path='/v1/account',
            json=json_data
        )
        return response

    # метод для активации токена
    def put_v1_account_token(self, token):
        """"
        Activate register user
        :param token:
        :return:
        """
        #headers = self.headers

        headers = {
            'accept': 'text/plain',
        }

        response = self.put(
            path=f'/v1/account/{token}',
            headers=headers
        )

        return response

    # метод для изменения имейла
    def put_v1_account_email(self, json_data):
        """"
        Change registered user email
        :param json_data:
        :param email:
        :return:
        """
        headers = {
            'accept': 'text/plain',
            'Content-Type': 'application/json',
        }

        response = self.put(
            path='/v1/account/email',
            headers=headers,
            json=json_data
        )
        return response

    # метод для получения пользователя
    def get_v1_account(self, **kwargs):
        """"
        Get current user
        :return:
        """

        response = self.get(
            path='/v1/account',
            **kwargs
        )
        return response