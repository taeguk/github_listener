#!/usr/bin/python3

#-*- coding: utf-8 -*-

from github_listener import GithubAccount
from github_listener.parser import NotificationParser

account = GithubAccount("username", "password")
parser = NotificationParser(account)
groups = parser.parse()

for group in groups:
    print("\n-- {0} --".format(group.group_name))
    idx = 1
    for n in group.notifications:
        print("#{0}\nTitle : {1}\nLink : {2}\nPersons : {3}".format(idx, n.title, n.link, n.persons))
        idx += 1
