__author__ = 'd9pouces'

import getpass

COMPANY = '19pouces.net'
try:
    AUTHOR = getpass.getuser()
except ImportError:
    AUTHOR = 'd9pouces'
