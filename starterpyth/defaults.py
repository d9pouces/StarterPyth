__author__ = 'flanker'

import getpass

COMPANY = '19pouces.net'
try:
    AUTHOR = getpass.getuser()
except ImportError:
    AUTHOR = 'flanker'