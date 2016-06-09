#-*- coding: utf-8 -*-

class GithubAccount:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        if not self.is_valid():
            raise ValueError('Account is invalid. Username or password is incorrect.')
        
    def is_valid(self):
        import requests
        r = requests.get('https://api.github.com/notifications', 
            auth = (self.username, self.password))
        if r.status_code == 401: # Not Authorized
            return False
        return True

class GithubAPI:
    def __init__(self, account):
        self.account = account
