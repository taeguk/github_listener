#-*- coding: utf-8 -*-

class GithubAccount:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class GithubAPI:
    def __init__(self, account):
        self.account = account
