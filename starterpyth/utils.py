"""
several utility functions:
  * unicode function to be compatible with both Python 2 & 3
  * copy of the :func:`os.walk` function, adapted to pkg_resources
"""
import unicodedata

import pkg_resources


__author__ = 'd9pouces'

__all__ = ['normalize_str', 'walk']


def normalize_str(orig_str):
    """
    Remove all Unicode-only characters and replace them by their ASCII equivalent.
    :param orig_str: str
    :return: str
    """
    return unicodedata.normalize('NFKD', orig_str).encode('ASCII', 'ignore').decode('utf-8')


if __name__ == '__main__':
    import doctest
    doctest.testmod()


def walk(module_name, dirname, topdown=True):
    """
    Copy of :func:`os.walk`. Please refer to its doc. The only difference is that we walk in a package_resource
    instead of a plain directory.
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
    return rec_walk(dirname)
