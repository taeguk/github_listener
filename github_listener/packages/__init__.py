from __future__ import absolute_import
import sys

try:
    from . import requests
except ImportError:
    import requests
    sys.modules['%s.requests' % __name__] = requests

try:
    from . import bs4
except ImportError:
    import bs4
    sys.modules['%s.bs4' % __name__] = bs4

