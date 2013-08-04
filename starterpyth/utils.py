import sys
import pkg_resources

__author__ = 'flanker'



if sys.version_info[0] == 3:
    my_unicode = str
else:
    my_unicode = lambda x: x.decode('utf-8')


def walk(module_name, dirname, topdown=True):
    def rec_walk(root):
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
    return rec_walk(my_unicode(dirname))


if __name__ == '__main__':
    import doctest
    doctest.testmod()