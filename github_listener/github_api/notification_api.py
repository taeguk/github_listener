#-*- coding: utf-8 -*-

import requests
from .github_api import (
    GithubAccount, 
    GithubAPI,
)

class Notification(object):
    def __init__(self, raw_json, title, link, person, text):
        self.raw_json = raw_json
        self.title = title
        self.link = link
        self.person = person
        self.text = text
        self.hash_val = self.__hash__()

    def __eq__(self, notification):
        return self.hash_val == notification.hash_val

    def __hash__(self):
        return hash(self.title + self.link + self.person + self.text)

class NotificationGroup(object):
    def __init__(self, group_name):
        self.group_name = group_name
        self.notifications = []

    def add_notification(self, notification):
        self.notifications.append(notification)

class NotificationAPI(GithubAPI):
    def __init__(self, account):
        super().__init__(account)
        self.last_modified_date = None

    def find_notification_group(self, groups, group_name):
        for group in groups:
            if group.group_name == group_name:
                return group
        return None

    def get_notification_groups(self, only_change = False):
        headers = {}
        if only_change and self.last_modified_date is not None:
            headers['If-Modified-Since'] = self.last_modified_date
        r = requests.get('https://api.github.com/notifications', 
            auth = (self.account.username, self.account.password),
            headers = headers)
        if r.status_code == 304: # Not Modified
            return []
        if only_change:
            self.last_modified_date = r.headers['Last-Modified']

        n_groups = []
        json_data_list = r.json()
        for json_data in json_data_list:
            raw_json = json_data
            repo_name = json_data['repository']['full_name']
            title = json_data['subject']['title']
            comment_api_url = json_data['subject']['latest_comment_url']
            r2 = requests.get(comment_api_url, auth=(self.account.username, self.account.password))
            comment_json_data = r2.json()
            link = comment_json_data['html_url']
            person = comment_json_data['user']['login']
            text = comment_json_data['body']

            n = Notification(raw_json, title, link, person, text)
            group = self.find_notification_group(n_groups, repo_name)
            if group is None:
                group = NotificationGroup(repo_name)
                n_groups.append(group)
            group.add_notification(n)

        return n_groups
