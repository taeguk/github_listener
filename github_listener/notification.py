#-*- coding: utf-8 -*-

from .github_api.github_api import GithubAccount
from .github_api.notification_api import (
    Notification,
    NotificationGroup,
    NotificationAPI,
)

class NotificationChange(object):
    def __init__(self, n_groups = []):
        self.n_groups = n_groups

    def add_change(self, group, n = None):
        if n is None:
            self.n_groups.append(group)
        else:
            n_group = self.find_or_add_group(group)
            n_group.add_notification(n)

    def find_or_add_group(self, group):
        for n_group in self.n_groups:
            if n_group.group_name == group.group_name:
                return n_group
        n_group = NotificationGroup(group.group_name)
        self.n_groups.append(n_group)
        return n_group

    def is_changed(self):
        return len(self.n_groups) >= 1

class NotificationChecker(object):
    def __init__(self, account):
        self.account = account
        self.notification_api = NotificationAPI(account)
        self.notification_change = None

    def check_notification(self):
        n_groups = self.notification_api.get_notification_groups(only_change = True)

        if self.notification_change is None:
            self.notification_change = NotificationChange()
        else:
            self.notification_change = NotificationChange(n_groups)

        return self.notification_change.is_changed()
