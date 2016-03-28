#-*- coding: utf-8 -*-

from .parser.github import GithubAccount
from .parser.notification_parser import (
    Notification,
    NotificationGroup,
    NotificationParser,
)

class NotificationChange(object):
    def __init__(self):
        self.n_groups = []

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
        self.prev_notification_groups = None
        self.change_notification = None

    def check_notification(self):
        parser = NotificationParser(self.account)
        cur_groups = parser.parse()

        if self.prev_notification_groups is None:
            self.prev_notification_groups = cur_groups
            return False

        prev_groups = sorted(self.prev_notification_groups, key=lambda x: x.group_name)
        self.prev_notification_groups = cur_groups
        cur_groups.sort(key=lambda x: x.group_name)
        prev_group_idx = cur_group_idx = 0
        prev_group_cnt = len(prev_groups)
        cur_group_cnt = len(cur_groups)

        self.change_notification = NotificationChange()
        while prev_group_idx < prev_group_cnt and cur_group_idx < cur_group_cnt:
            prev_group = prev_groups[prev_group_idx]
            cur_group = cur_groups[cur_group_idx]

            if prev_group.group_name < cur_group.group_name:
                prev_group_idx += 1
            elif prev_group.group_name > cur_group.group_name:
                self.change_notification.add_change(cur_group)
                cur_group_idx += 1
            else:
                prev_set = set(prev_group.notifications)
                cur_set = set(cur_group.notifications)
                change_set = cur_set - prev_set
                for n in change_set:
                    self.change_notification.add_change(cur_group, n)
                prev_group_idx += 1
                cur_group_idx += 1
                
        while cur_group_idx < cur_group_cnt:
            self.change_notification.add_change(cur_groups[cur_group_idx])
            cur_group_idx += 1
        

        return self.change_notification.is_changed()

    def notification_groups_to_notifications(self, n_groups):
        n_list = []
        for n_group in n_groups:
            n_list.append(n_group.notifications)
        return n_list

