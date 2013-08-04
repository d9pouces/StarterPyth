import copy
import logging
from io import BytesIO
import traceback
import sys

__author__ = 'flanker'
__all__ = ['ColorizedHandler', 'traceback', 'CONSOLE']


class ColorizedHandler(logging.StreamHandler):
    """Basic :class:`logging.StreamHandler` modified to colorize its output
    according to the record level.
    """

    def emit(self, record):
        """If a formatter is specified, it is used to format the record. The
        record is the written to the stream with a new line terminator.
        If exception information is present, it is formatted using
        :param record: record to emit
        :func:`traceback.print_exception()` and appended to the stream.
        The message is colorized according to the level of the record:
          * :attr:`logging.debug` => pink
          * :attr:`logging.info` => green
          * :attr:`logging.warning` => yellow
          * :attr:`logging.error` => red
        """
        myrecord = copy.copy(record)
        levelno = myrecord.levelno
        if levelno >= 50:
            color = '\x1b[31m'  # red
        elif levelno >= 40:
            color = '\x1b[31m'  # red
        elif levelno >= 30:
            color = '\x1b[33m'  # yellow
        elif levelno >= 20:
            color = '\x1b[32m'  # green
        elif levelno >= 10:
            color = '\x1b[35m'  # pink
        else:
            color = '\x1b[0m'  # normal
        myrecord.msg = color + myrecord.msg + '\x1b[0m'  # normal
        return logging.StreamHandler.emit(self, myrecord)


def log_traceback(error, msg=None):
    """
    Log a traceback
    :param error: error
    :param msg: message to prefix tracebacks with
    """
    if msg is not None:
        logging.error(msg)
    o = BytesIO()
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_tb(exc_traceback, file=o)
    logging.error('{0}: {1}'.format(error.__class__.__name__, error))
    logging.error(o.getvalue())


CONSOLE = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'color': {
            'level': 'DEBUG',
            'filters': [],
            'class': 'starterpyth.log.ColorizedHandler'
        }
    },
    'root': {
        'handlers': ['color'],
        'level': 'DEBUG',
        'propagate': True,
    }
}


if __name__ == '__main__':
    import doctest
    doctest.testmod()