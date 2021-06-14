import json
import pathlib
from time import time
from urllib.parse import urlencode
from hashlib import sha512

import re
from CodeforcesAPI.APIRequest import call_api


class CodeforcesBlogEntry:
    parent = None
    blog_entry_id = None
    blog = {}

    def get(self):
        return self.blog

    def view(self):
        """
        Get Blog entry

        :return: <dict> Blog entry
        """
        entry = call_api(self.parent, 'blogEntry.view', data={
            'blogEntryId': self.blog_entry_id
        }, cache_time=24 * 60 * 60)
        return entry

    def comments(self):
        """
        Get Blog entry comments

        :return: <list <dict>> Blog entry comments
        """
        comments = call_api(self.parent, 'blogEntry.comments', data={
            'blogEntryId': self.blog_entry_id
        }, cache_time=24 * 60 * 60)
        return comments

    def __init__(self, parent, blog_entry_id='', blog=None):
        """
        :param blog_entry_id: blog entry id
        :param parent: instanceof **Codeforces**
        """
        self.blog_entry_id = blog_entry_id
        if blog is not None:
            self.blog = blog
            self.blog_entry_id = blog['id']
        else:
            self.blog['id'] = self.blog_entry_id
        self.parent = parent
