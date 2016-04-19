#-*- coding: utf-8 -*-

import time
from .github_api.github_api import GithubAccount
from .notification import (
    NotificationChange,
    NotificationChecker,
)

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

GithubEvents = enum("notification")

class HandlerManager(object):
    def __init__(self):
        self.notification_handler = self.default_handler

    def default_handler(self):
        pass

    def do_handler(self, event, data):
        if event == GithubEvents.notification:
            self.notification_handler(data)
        else:
            raise Exception("Unknown github event.")

class GithubEventChecker(object):
    def __init__(self, account):
        self.account = account
        self.notification_checker = NotificationChecker(account)

    def get_change(self, event):
        if event == GithubEvents.notification:
            return self.notification_checker.notification_change
        else:
            raise Exception("Unknown github event.")

    def check_all_events(self):
        events = []
        if self.notification_checker.check_notification():
            events.append(GithubEvents.notification)
        return events

class GithubListener(object):
    def __init__(self, account):
        self.handler_manager = HandlerManager()
        self.event_checker = GithubEventChecker(account)
        self.account = account

    def notification(self, callback):
        def handler(change):
            callback(change)
        self.handler_manager.notification_handler = handler
        return callback

    def check_event_occurrence(self):
        events = self.event_checker.check_all_events()
        return events

    def process_events(self, events):
        for event in events:
            self.handler_manager.do_handler(event, self.event_checker.get_change(event))

    def run(self, sleep_sec = 0.5):
        while True:
            events = self.check_event_occurrence()
            self.process_events(events)
            time.sleep(sleep_sec)

if __name__ == "__main__":
    pass
