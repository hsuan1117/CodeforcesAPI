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

    # Data Properties
    session = None
    handle = None
    password = None
    apiKey = ''
    secret = ''
    contestId = ''
    groupId = ''
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
            handle=os.environ.get('HANDLE'),
            password=os.environ.get('PASSWORD'),
            api_key=os.environ.get('API_KEY'),
            secret=os.environ.get('SECRET'),
            contest_id=os.environ.get('CONTEST_ID'),
            group_id=os.getenv('GROUP_ID'),
            cache=True,
            session=Session()
    ):
        self.handle = handle
        self.password = password
        self.apiKey = api_key
        self.secret = secret
        self.session = session
        self.contestId = contest_id
        self.groupId = group_id
        self.cache = cache

    def dump(self):
        print(self.handle)
