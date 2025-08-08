import requests

class AccountApi:
    def __init__(self, host, headers=None):
        self.host = host
        self.headers = headers

    def get_headers(self):
        return self.headers

    # метод для регистрации пользователя
    def post_account(self, json_data):
        """"
        Register new user
        :param json_data:
        :return:
        """
        #headers = self.headers

        response = requests.post(url=f'{self.host}/v1/account',
                                 #headers=headers,
                                 json=json_data
                                 )

        return response

    # метод для активации токена
    def put_account_token(self, token):
        """"
        Activate register user
        :param token:
        :return:
        """
        headers = self.headers

        headers = {
            'accept': 'text/plain',
        }

        response = requests.put(url=f'{self.host}/v1/account/{token}',
                                headers=headers
                                )

        return response

    # метод для изменения имейла
    def put_account_email(self, json_data):
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


        response = requests.put(url=f'{self.host}/v1/account/email',
                                headers=headers,
                                json=json_data
                                )
        return response