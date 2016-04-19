#!/usr/bin/python3

#-*- coding: utf-8 -*-

from github_listener import GithubAccount
from github_listener.github_api import NotificationAPI

account = GithubAccount("username", "password")
api = NotificationAPI(account)
groups = api.get_notification_groups()

for group in groups:
    print("\n-- {0} --".format(group.group_name))
    idx = 1
    for n in group.notifications:
        print("#{0}\nTitle : {1}\nLink : {2}\nPerson : {3}\nText : {4}".format(idx, n.title, n.link, n.person, n.text))
        idx += 1
