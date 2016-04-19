Github Listener
=====================

.. image:: https://img.shields.io/pypi/v/github_listener.svg
    :target: https://pypi.python.org/pypi/github_listener

.. image:: https://img.shields.io/pypi/dm/github_listener.svg
    :target: https://pypi.python.org/pypi/github_listener

The simple library that calls user's registered functions whenever github events happen.


How to install
-----------------

You can install Github Listener using pip :

.. code-block:: bash

    $ pip install github_listener


Feature Support
--------------------

- Notification
- ...If you have things you want, please tell me through issues_.

.. _issues: https://github.com/taeguk/github_listener/issues


Example
---------------

.. code-block:: python

    from github_listener import (
      GithubAccount,
      GithubListener,
    )
    
    account = GithubAccount("username", "password")
    listener = GithubListener(account)
    
    @listener.notification
    def on_notification(change):
      # Do things that you want to do whenever the github's notification occurs.
      pass
    
    listener.run()  # infinite loop


.. code-block:: python

    from github_listener import GithubAccount
    from github_listener.github_api import NotificationAPI

    account = GithubAccount("username", "password")
    api = NotificationAPI(account)
    groups = api.get_notification_groups()
    
    # Do something using notification informations.

For more detail examples, Go Examples_.

.. _Examples: https://github.com/taeguk/github_listener/tree/master/examples


Contribution
-----------------
Welcome any kind of contribution!
