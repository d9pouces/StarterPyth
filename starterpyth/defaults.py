from six import u
import six

__author__ = 'd9pouces'

import getpass

COMPANY = u('19pouces.net')
try:
    AUTHOR = getpass.getuser()
    if isinstance(AUTHOR, six.binary_type):
        AUTHOR = AUTHOR.decode('utf-8')
except ImportError:
    AUTHOR = u('d9pouces')
