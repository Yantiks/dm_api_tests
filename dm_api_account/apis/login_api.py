import requests
from restclient.client import RestClient

class LoginApi(RestClient):

    # логин пользователя
    def post_v1_account_login(self, json_data):
        """"
        Authenticate via credentials
        :param json_data:
        :return:
        """
        headers = {
            'accept': 'text/plain',
            'Content-Type': 'application/json',
        }

        response = self.post(
            path='/v1/account/login',
            headers=headers,
            json=json_data
        )
        return response

    def delete_v1_account_login(self):
        """"
        Logout as current user
        :return:
        """

        response = self.delete(
            path='/v1/account/login'
        )
        return response

    def delete_v1_account_login_all(self):
        """"
        Logout from every device
        :return:
        """

        response = self.delete(
            path='/v1/account/login/all'
        )
        return response