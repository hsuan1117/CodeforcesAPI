import json
import pathlib
from time import time
from urllib.parse import urlencode
from hashlib import sha512

import re
from CodeforcesAPI.APIRequest import call_api


class CodeforcesUser:
    parent = None
    user_id = None
    user = {}

    def get(self):
        return self.user

    def info(self, data=None):
        """
        Get User information

        :param data: other data to send
        :return: <dict> User info
        """
        info = call_api(self.parent, 'user.info', data={
            'handles': self.user_id
        }, cache_time=24 * 60 * 60)
        return info[0]

    def rating(self, data=None):
        """
        Get User rating

        :param data: other data to send
        :return: <dict> Rating Information
        """
        info = call_api(self.parent, 'user.rating', data={
            'handle': self.user_id
        }, cache_time=60 * 60)
        return info

    def submissions(self, data=None):
        """
        Get User submissions

        :param data: other data to send
        :return: <dict> User submissions
        """
        info = call_api(self.parent, 'user.status', data={
            'handle': self.user_id
        }, cache_time=60 * 60)
        return info

    def friends(self):
        """
        Get User authorized friend (depends on apiKey)

        :return: <list <CodeforcesUser>> User friends
        """
        friends = call_api(self.parent, 'user.friends', data={
            'handle': self.parent.apiKey
        }, cache_time=24 * 60 * 60)
        return [CodeforcesUser(self.parent, user_id=user) for user in friends]

    def blogs(self):
        """
        Get User blogs

        :return: <list <CodeforcesBlogEntry>> User blogs entries
        """
        entries = call_api(self.parent, 'user.blogEntries', data={
            'handle': self.user_id
        }, cache_time=24 * 60 * 60)
        from CodeforcesAPI.Blogs import CodeforcesBlogEntry
        return [CodeforcesBlogEntry(self.parent, blog_entry_id=entry) for entry in entries]

    def __init__(self, parent, user_id='', user=None):
        """
        :param user_id: user id
        :param parent: instanceof **Codeforces**
        """
        self.user_id = user_id
        if user is not None:  # if have user, use its id
            self.user = user
            self.user_id = user['id']
        else:
            self.user['id'] = self.user_id
        self.parent = parent
