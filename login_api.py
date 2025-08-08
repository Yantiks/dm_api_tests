import requests

class LoginApi:
    def __init__(self, host, headers=None):
        self.host = host
        self.headers = headers

    # логин пользователя
    def post_account_login(self, json_data):
        """"
        Authenticate via credentials
        :param json_data:
        :return:
        """
        headers = {
            'accept': 'text/plain',
            'Content-Type': 'application/json',
        }

        json_data = {
            'login': 'string',
            'password': 'string',
            'rememberMe': True,
        }

        response = requests.post(url=f'{self.host}/v1/account/login',
                                 headers=headers,
                                 json=json_data
                                 )

        return response
