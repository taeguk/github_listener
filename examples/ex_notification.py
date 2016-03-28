#!/usr/bin/python3

#-*- coding: utf-8 -*-

from github_listener import (
    GithubAccount,
    GithubListener,
)

account = GithubAccount("username", "password")
listener = GithubListener(account)

@listener.notification
def on_change(change):
    print("[*] on_change()")
    for group in change.n_groups:
        print("-- {0} --".format(group.group_name))
        idx = 1
        for n in group.notifications:
            print("#{0}\nTitle : {1}\nLink : {2}\nPersons : {3}".format(idx, n.title, n.link, n.persons))
            idx += 1

print("- start -")
listener.run()
print("- end -")
