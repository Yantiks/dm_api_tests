from restclient.configuration import Configuration
from api_mailhog.apis.mail_api import MailApi

class MailhogApi:
    def __init__(self, configuration: Configuration):
        self.configuration = configuration
        self.mailhog_api = MailApi(configuration=self.configuration)
