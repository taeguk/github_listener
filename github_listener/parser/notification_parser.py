#-*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from ..github_listener import GithubAccount
from ..notification import NotificationGroup

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



