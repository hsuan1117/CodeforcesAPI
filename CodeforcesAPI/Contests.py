import json
import pathlib
from time import time
from urllib.parse import urlencode
from hashlib import sha512

import re
from CodeforcesAPI.APIRequest import call_api


def process_submission_details(submission):
    # print('[Submission Detail]: ' + submission)
    start = 0
    place = submission.find('Group')
    subtasks = []
    while place >= 0:
        start = place + 1
        place = submission.find(':', start)
        for i in range(place + 2, place + 10):
            if submission[i] == ' ':
                subtasks.append(float(submission[place + 2: i]))
                break
        place = submission.find('Group', start)
    return subtasks


class CodeforcesContest:
    parent = None

    def info(self, data=None):
        return self.standings(data=(data or None))['contest']

    def users(self, data=None):
        result = self.status(data=(data or None))
        user_list = set()
        for submission in result:
            for user in submission['author']['members']:
                user_list.add(user['handle'])
        user_list = list(user_list)
        return user_list

    def problems(self, data=None):
        return self.standings(data=(data or None))['problems']

    def submissions(self, data=None, ignore_manager=True, ignore_out_of_time=True, ignore_zero_point=True,
                    with_subtasks=False, with_simple_handle=False, with_simple_problem=False):
        """
        :param with_simple_problem:
        :param with_simple_handle:
        :param with_subtasks:
        :param ignore_zero_point:
        :param ignore_out_of_time:
        :param ignore_manager:
        :param data:
        :return:
        """
        result = self.status(data=(data or None))
        submissions_list = []
        for submission_info in result:
            if ignore_manager and submission_info['author']['participantType'] == 'MANAGER':
                continue
            if ignore_out_of_time and submission_info['relativeTimeSeconds'] == 2147483647:
                continue
            if ignore_zero_point and submission_info['points'] == 0.0:
                continue
            if with_subtasks:
                submission_info['subtasks'] = process_submission_details(self.submission_details(submission_info['id']))
            if with_simple_handle:
                submission_info['handle'] = submission_info['author']['members'][0]['handle']
                submission_info.pop('author', None)
            if with_simple_problem:
                submission_info['problem'] = {
                    'index': submission_info['problem']['index'],
                    'name': submission_info['problem']['name']
                }

            submissions_list.append(submission_info)
        return submissions_list

    def submission_details(self, submission_id, cache_time=None, force_login=False):
        """
        :param force_login:
        :param cache_time:
        :param submission_id: required
        :return:
        """
        if self.parent.handle is None or self.parent.password is None:
            from CodeforcesAPI import CodeforcesCredentialException
            raise CodeforcesCredentialException(message='Handle and password is required.')

        cache_file = None
        if self.parent.cache:  # 如果要cache
            pathlib.Path('cache/').mkdir(parents=True, exist_ok=True)
            cache_file = pathlib.Path(f'cache/submission-{submission_id}.txt')

            if cache_file.exists() and cache_file.stat().st_size != 0 and int(time()) - int(
                    cache_file.stat().st_mtime) < (cache_time or 24 * 60 * 60):
                cache = cache_file.open('r', encoding="utf-8")
                return cache.read()
        if not self.parent.isLoggedIn or force_login:
            self.parent.login()
        res = self.parent.session.get('https://codeforces.com')
        csrf_token = re.findall('<meta name="X-Csrf-Token" content="(.{32})"/>', res.text)[0]
        data = {
            'csrf_token': csrf_token,
            'submissionId': submission_id,
        }
        res = self.parent.session.post(f"https://codeforces.com/group/{self.parent.groupId}/data/judgeProtocol",
                                       data=data)
        if "html" in res.text:
            from CodeforcesAPI import CodeforcesCredentialException
            raise CodeforcesCredentialException()
        cache = cache_file.open('w+', encoding="utf-8")
        cache.write(res.text)
        return res.text

    def status(self, data=None):
        default_data = {
            'contestId': self.parent.contestId
        }
        if data is None:
            data = {}

        final_data = {**default_data, **data}

        return call_api(parent=self.parent, data=final_data)

    def standings(self, data=None):
        default_data = {
            'contestId': self.parent.contestId
        }
        if data is None:
            data = {}
        final_data = {**default_data, **data}
        result = call_api(parent=self.parent, endpoint='contest.standings', data=final_data)
        return result

    def __init__(self, parent):
        self.parent = parent

    # Dummy Functions
    tasks = problems
