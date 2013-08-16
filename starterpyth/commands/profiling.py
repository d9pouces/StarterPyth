from starterpyth.utils import my_unicode

__author__ = 'd9pouces'

from distutils.core import Command
import os.path
import logging
import pdb
import sys
import token
import tokenize

try:
    import cProfile as profile
except ImportError:
    import profile
if sys.version[0] < 3:
    try:
        from cStringIO import StringIO as BytesIO
    except ImportError:
        from StringIO import StringIO as BytesIO
else:
    from io import BytesIO


class Profiling(Command):
    """Provide shortcuts for debugging and profiling functions"""
    description = 'Provide shortcuts for debugging and profiling functions'
    user_options = [
        ('output=', 'o', "file to output profiling data"),
        ('input=', 'i', "file from which read profiling data"),
        ('call=', 'c', "function to profile"),
        ('debug', 'd', "debug function instead of profiling it"),
    ]

    def initialize_options(self):
        self.output = None
        self.input = None
        self.call = None
        self.debug = 0

    def finalize_options(self):
        pass

    def run(self):
        if self.input:
            try:
                # noinspection PyUnresolvedReferences
                import pstats
            except ImportError:
                logging.error('Module pstats not found.')
                return
            if not os.path.isfile(self.input):
                logging.error(my_unicode('File %s not found' % self.input))
                return
            stats = pstats.Stats(self.input)
            stats.print_stats()
        elif not self.call:
            logging.error('Please provide a function to profile with --call \'module.function\'')
            return
        else:
            if '(' not in self.call:
                self.call += '()'
            tokens = tokenize.generate_tokens(BytesIO(self.call).readline)
            index = 0
            simple_function_call = True
            for toknum, tokval, tokstart, tokend, tokline in tokens:
                if toknum == token.ENDMARKER:
                    break
                elif index == 0 and toknum != token.NAME:
                    simple_function_call = False
                    break
                elif index == 1 and toknum == token.OP and tokval == '(':
                    break
                elif index == 1 and (toknum != token.OP or tokval != '.'):
                    simple_function_call = False
                    break
                index = 1 - index
            if simple_function_call:
                module_name = self.call.partition('(')[0].rpartition('.')[0]
                if module_name:
                    logging.info('Load module %s' % module_name)
                    self.call = 'import %s ; %s' % (module_name, self.call)
            logging.info("running profiling on %(call)s" % {'call': self.call})
            if self.debug:
                pdb.run(self.call)
            else:
                profile.run(self.call, self.output)
