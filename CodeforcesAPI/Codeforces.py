import os
import re

from dotenv import load_dotenv
from requests import Session
from CodeforcesAPI.Exceptions import CodeforcesException, CodeforcesCredentialException, CodeforcesSessionException
from CodeforcesAPI.Contests import CodeforcesContest

load_dotenv()


class Codeforces:
    # Status Properties
    isLoggedIn = False
    # parse = False

    # Data Properties
    session = None
    handle = None
    password = None
    apiKey = ''
    secret = ''
    cache = True

    # 所有參數在init設定，不然就在env設定

    def login(self):
        if self.session is not None:
            res = self.session.get('https://codeforces.com/enter')
            csrf_token = re.findall('<meta name="X-Csrf-Token" content="(.{32})"/>', res.text)[0]
            data = {
                'csrf_token': csrf_token,
                'action': 'enter',
                'ftaa': '',
                'bfaa': '',
                'handleOrEmail': self.handle,
                'password': self.password
            }
            res = self.session.post('https://codeforces.com/enter', data=data)
            if 'Logout' in res.text:
                self.isLoggedIn = True
            else:
                raise CodeforcesCredentialException()
        else:
            raise CodeforcesSessionException()

    def logout(self):
        if self.session is not None:
            res = self.session.get('https://codeforces.com')
            link = re.findall('<a href="(/.{32}/logout)">Logout</a>', res.text)[0]
            res = self.session.get('https://codeforces.com' + link)
            if 'Logout' not in res.text:
                self.isLoggedIn = False
            else:
                raise CodeforcesSessionException()
        else:
            raise CodeforcesSessionException()

    def contest(self):
        return CodeforcesContest(self)

    def __init__(
            self,
            handle=None,
            password=None,
            api_key=None,
            secret=None,
            contest_id=None,
            group_id=None,
            cache=True,
            session=None,
            # parse=True
    ):
        """

        :param handle: Codeforces Handle defaults to os.environ.get('HANDLE')
        :param password: Codeforces Password defaults to os.environ.get('PASSWORD')
        :param api_key: Codeforces API Key defaults to os.environ.get('API_KEY')
        :param secret: Codeforces API Secret defaults to os.environ.get('SECRET')
        :param cache: whether using cache defaults to True
        :param session: defaults to Session()
        :param @deprecated parse: defaults to True
        """
        self.handle = handle or os.environ.get('HANDLE')
        self.password = password or os.environ.get('PASSWORD')
        self.apiKey = api_key or os.environ.get('API_KEY')
        self.secret = secret or os.environ.get('SECRET')
        self.session = session or Session()
        self.cache = cache
        # self.parse = parse

    def dump(self):
        print(self.handle)
