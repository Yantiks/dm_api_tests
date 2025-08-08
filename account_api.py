import requests

class AccountApi:
    def __init__(self, host, headers=None):
        self.host = host
        self.headers = headers

    def get_headers(self):
        return self.headers

    # метод для регистрации пользователя
    def post_account(self, json_data):
        headers = self.headers

        json_data = {
            'login': 'string',
            'email': 'string',
            'password': 'string',
        }

        response = requests.post('http://5.63.153.31:5051/v1/account', headers=headers, json=json_data)

        return response

    # метод для активации токена
    def put_account_token(self, token):
        headers = self.headers

        headers = {
            'accept': 'text/plain',
        }

        response = requests.put(f'http://5.63.153.31:5051/v1/account/{token}',
                                headers=headers)

        return response

    # метод для изменения имейла
    def put_account_email(self, json_data,email):
        headers = {
            'accept': 'text/plain',
            'Content-Type': 'application/json',
        }

        json_data = {
            'login': 'string',
            'password': 'string',
            'email': 'string',
        }

        response = requests.put(f'http://5.63.153.31:5051/v1/account/{email}', headers=headers, json=json_data)
        return response