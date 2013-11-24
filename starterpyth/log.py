import traceback
import sys
from six import u, StringIO

__author__ = 'd9pouces'
__all__ = ['red', 'print_tb', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']


def __add_color(code):
    def __wrapped(text, bold=False):
        if bold:
            return u("\033[1;{0}m{1}\033[0m").format(code, text)
        return u("\033[{0}m{1}\033[0m").format(code, text)
    return __wrapped

red = __add_color(u('31'))
green = __add_color(u('32'))
yellow = __add_color(u('33'))
blue = __add_color(u('34'))
magenta = __add_color(u('35'))
cyan = __add_color(u('36'))
white = __add_color(u('37'))


def print_tb(error, msg=None):
    """
    Log a traceback
    :param error: error
    :param msg: message to prefix tracebacks with
    """
    if msg is not None:
        print(red(msg))
    out_buf = StringIO()
    exc_traceback = sys.exc_info()[2]
    traceback.print_tb(exc_traceback, file=out_buf)
    print(red('{0}: {1}'.format(error.__class__.__name__, error)))
    print(yellow(out_buf.getvalue()))


if __name__ == '__main__':
    import doctest
    doctest.testmod()
