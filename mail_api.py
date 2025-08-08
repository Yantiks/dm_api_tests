import requests
import loads

class MailApi:
    def __init__(self, host, headers=None):
        self.host = host
        self.headers = headers

    # получение токена с почты
    def get_messages(self, limit=50):
        """"
        Ger users emails
        :param limit:
        :return:
        """

        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        }

        params = {
            'limit': limit,
        }

        response = requests.get(url=f'{self.host}/api/v2/messages',
                                params=params,
                                headers=headers,
                                verify=False
                                )
        return response

    def get_activation_token(self, login, response):
        token = None

        for item in response.json()['items']:
            user_data = loads(item['Content']['Body'])
            user_login = user_data['Login']
            if user_login == login:
                token = user_data['ConfirmationLinkUrl'].split('/')[-1]
        return token