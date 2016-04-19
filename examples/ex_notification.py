#!/usr/bin/python3

#-*- coding: utf-8 -*-

from github_listener import (
    GithubAccount,
    GithubListener,
)

account = GithubAccount("username", "password")
listener = GithubListener(account)

@listener.notification
def on_notification(change):
    print("[*] notification occurs!")
    for group in change.n_groups:
        print("-- {0} --".format(group.group_name))
        idx = 1
        for n in group.notifications:
            print("#{0}\nTitle : {1}\nLink : {2}\nPerson : {3}\nText : {4}".format(idx, n.title, n.link, n.person, n.text))
            idx += 1

print("- start -")
listener.run()  # infinite loop
# listener.run(5)   # listener sleep 5 seconds whenever processing is finished.
print("- end -")
