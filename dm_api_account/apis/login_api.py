import requests

class LoginApi:
    def __init__(self, host, headers=None):
        self.host = host
        self.headers = headers

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



        response = requests.post(url=f'{self.host}/v1/account/login',
                                 headers=headers,
                                 json=json_data
                                 )

        return response
