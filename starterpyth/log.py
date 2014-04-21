import traceback
import sys
from six import u, b, StringIO, text_type, print_

__author__ = 'd9pouces'
__all__ = ['print_tb', 'display', 'RED', 'GREEN', 'YELLOW', 'BLUE', 'MAGENTA', 'CYAN', 'WHITE']


RED = '31'
GREEN = '32'
YELLOW = '33'
BLUE = '34'
MAGENTA = '35'
CYAN = '36'
WHITE = '37'


__encode_stdout = not (hasattr(sys.stdout, 'encoding') and sys.stdout.encoding.lower() == 'utf-8')


def display(text, color=None, bold=False, newline=True):
    if not isinstance(text, text_type):
        text = text.decode('utf-8')
    if bold and color:
        text = u("\033[1;{0}m{1}\033[0m").format(color, text)
    text = u("\033[{0}m{1}\033[0m").format(color, text)
    if newline:
        text += u('\n')
    end = u('')
    if __encode_stdout:
        text = text.encode('utf-8')
        end = b('')
    print_(text, end=end)


def print_tb(error, msg=None):
    """
    Log a traceback
    :param error: error
    :param msg: message to prefix tracebacks with
    """
    if msg is not None:
        display(msg, color=RED, bold=True)
    out_buf = StringIO()
    exc_traceback = sys.exc_info()[2]
    traceback.print_tb(exc_traceback, file=out_buf)
    display('{0}: {1}'.format(error.__class__.__name__, error), color=RED)
    display(out_buf.getvalue(), color=YELLOW)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
