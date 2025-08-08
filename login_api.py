import requests

class LoginApi:
    def __init__(self, host, headers=None):
        self.host = host
        self.headers = headers

    # логин пользователя
    def post_account_login(self, json_data):
        headers = {
            'accept': 'text/plain',
            'Content-Type': 'application/json',
        }

        json_data = {
            'login': 'string',
            'password': 'string',
            'rememberMe': True,
        }

        response = requests.post('http://5.63.153.31:5051/v1/account/login', headers=headers, json=json_data)
        return response
