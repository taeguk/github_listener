#-*- coding: utf-8 -*-

from .packages import requests
from .packages.bs4 import BeautifulSoup

class Notification(object):
    def __init__(self, title, link, persons):
        self.title = title
        self.link = link
        self.persons = persons
        self.hash_val = self.__hash__()#hashlib.sha512(title + link + persons).hexdigest()

    def __eq__(self, notification):
        return self.hash_val == notification.hash_val

    def __hash__(self):
        return hash(self.title + self.link + self.persons)

class NotificationGroup(object):
    def __init__(self, group_name):
        self.group_name = group_name
        self.notifications = []

    def add_notification(self, notification):
        self.notifications.append(notification)

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

class NotificationParser(object):
    def __init__(self, account):
        self.account  = account

    def parse(self):
        notification_groups = []

        ID = self.account.username
        PW = self.account.password

        r = requests.get("https://github.com/login")

        if r.status_code != 200:
            raise Exception("Mistery Error")

        soup = BeautifulSoup(r.text, 'html.parser')
        CSRF_TOKEN = soup.find(attrs={"name": "authenticity_token"})['value']

        r = requests.post("https://github.com/session",
            data = {"commit" : "Sign in", "utf8" : "%E2%9C%93", "authenticity_token" : CSRF_TOKEN,
                    "login" : ID, "password" : PW}, cookies=r.cookies)

        if r.status_code != 200:
            raise Exception("Login Error")

        soup = BeautifulSoup(r.text, 'html.parser')
        alert_box = soup.find(id='js-flash-container')
        if str(alert_box).find("Incorrect") >= 0:
            raise Exception("Login Fail")

        r = requests.get("https://github.com/notifications", cookies=r.cookies)

        if r.status_code != 200:
            raise Exception("Loading Error")

        soup = BeautifulSoup(r.text, 'html.parser')
        target_area = soup.find_all(class_="notifications-list")[0]

        raw_group_list = target_area.find_all(class_="js-notifications-browser", recursive=False)
        for raw_group in raw_group_list:
            group_name = raw_group.h3.a.get_text().strip()
            raw_n_list = raw_group.ul.find_all('li', recursive=False)
            notification_group = NotificationGroup(group_name)
            notification_groups.append(notification_group)
            for raw_n in raw_n_list:
                n_title = raw_n.span.a.get_text().strip()
                n_link = raw_n.span.a.get('href').strip()
                n_persons = raw_n.ul.find_all(class_='tooltipped', recursive=False)[0].get('aria-label').strip()
                notification_group.add_notification(Notification(n_title, n_link, n_persons))

        return notification_groups

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

