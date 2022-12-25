import logging
import requests
import re
from bs4 import BeautifulSoup

class Pulsalapak:
    def __init__(self, user_id, user_key):
        '''
        Create a Pulsalapak instance.
        '''

        self.req = requests.Session()
        self.csrf = None

        self.req.cookies.set('user_id', user_id)
        self.req.cookies.set('user_key', user_key)
        logging.debug("Pulsalapak instance created.")

    def login(self):
        '''
        Logging in to Pulsalapak and get csrf token.
        '''

        logging.debug("Logging in to pulsalapak...")
        self.req.get('https://pulsalapak.com/akun/profil')
        csrf = self.req.cookies.get('csrf_cookie')

        if csrf is not None:
            self.csrf = csrf
            logging.debug("Got csrf token: %s", csrf)
        else: raise LoginError('Failed to get csrf token.')

    def create_deposit(self, amount, qrtype):
        '''
        Create qr code to deposit
        '''

        logging.debug("Creating deposit qr code...")
        res = self.req.post(
            "https://pulsalapak.com/akun/deposit",
            data={
                'csrf_token': self.csrf,
                'amount': str(amount),
                'payment': str(qrtype)
            })

        if res.status_code == 200 and \
        res.url.startswith("https://pulsalapak.com/akun/deposit/view/"):
            logging.debug("QR Code created successfully! (%s)", res.url)

            try:
                soup = BeautifulSoup(res.text, features="html.parser")
                data = soup.find_all('script')
                code = str(data[4].text)
                
                code = re.search("(?P<url>https?://[^\s]+)", code).group("url").replace("\",", "")
                return self.req.get(code).text
            except BaseException as exc: raise GetCodeError("Unable to get created qr code") from exc

        else: raise CreateError(f"Unable to create qr code ({res.status_code})")

class LoginError(BaseException):
    def __init__(self, message):
        '''
        Pulsalapak login error class.
        '''

        super().__init__(message)

class CreateError(BaseException):
    def __init__(self, message):
        '''
        Pulsalapak create error class.
        '''

        super().__init__(message)

class GetCodeError(BaseException):
    def __init__(self, message):
        '''
        Pulsalapak get code error class.
        '''

        super().__init__(message)