"""
several utility functions:
  * unicode function to be compatible with both Python 2 & 3
  * copy of the :func:`os.walk` function, adapted to pkg_resources
"""
import sys
import pkg_resources
import unicodedata

__author__ = 'd9pouces'


if sys.version_info[0] == 3:
    def py3k_unicode(raw_str):
        return str(raw_str)
else:
    def py3k_unicode(raw_str):
        if isinstance(raw_str, str):
            return raw_str.decode('utf-8')
        return raw_str


def normalize_str(orig_str):
    """
    Remove all Unicode-only characters and replace them by their ASCII equivalent.
    :param orig_str:
    :return:
    """
    return unicodedata.normalize('NFKD', orig_str).encode('ASCII', 'ignore')


def walk(module_name, dirname, topdown=True):
    """
    Copy of :func:`os.walk`. Please refer to this doc.
    :type module_name: basestring
    :param module_name: module to search in
    :type dirname: basestring
    :param dirname: base directory
    :type topdown: bool
    :param topdown: if True, perform a topdown search.
    """
    def rec_walk(root):
        """
        Recursively list subdirectories and filenames from the root.
        :param root: the root path
        :type root: basestring
        """
        dirnames = []
        filenames = []
        for name in pkg_resources.resource_listdir(module_name, root):
            fullname = root + '/' + name
            isdir = pkg_resources.resource_isdir(module_name, fullname)
            if isdir:
                dirnames.append(name)
                if not topdown:
                    rec_walk(fullname)
            else:
                filenames.append(name)
        yield root, dirnames, filenames
        if topdown:
            for name in dirnames:
                for values in rec_walk(root + '/' + name):
                    yield values
    return rec_walk(py3k_unicode(dirname))


if __name__ == '__main__':
    import doctest
    doctest.testmod()
