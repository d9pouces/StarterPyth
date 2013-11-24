from six import u, BytesIO
from starterpyth.log import red, green

__author__ = 'd9pouces'

from distutils.core import Command
import os.path
import pdb
import token
import tokenize

try:
    #noinspection PyPep8Naming
    import cProfile as profile
except ImportError:
    import profile


class Profiling(Command):
    """Provide shortcuts for debugging and profiling functions"""
    description = 'Provide shortcuts for debugging and profiling functions'
    user_options = [
        ('output=', 'o', "file to output profiling data"),
        ('input=', 'i', "file from which read profiling data"),
        ('call=', 'c', "function to profile"),
        ('debug', 'd', "debug function instead of profiling it"),
    ]

    def __init__(self, dist=None):
        super(Profiling, self).__init__(dist=dist)
        self.output = None
        self.input = None
        self.call = None
        self.debug = 0

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
                print(red('Module pstats not found.'))
                return
            if not os.path.isfile(self.input):
                print(red(u('File %s not found' % self.input)))
                return
            stats = pstats.Stats(self.input)
            stats.print_stats()
        elif not self.call:
            print(red('Please provide a function to profile with --call \'module.function\''))
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
                    print(green('Load module %s' % module_name))
                    self.call = 'import %s ; %s' % (module_name, self.call)
            print(green("running profiling on %(call)s" % {'call': self.call}))
            if self.debug:
                pdb.run(self.call)
            else:
                profile.run(self.call, self.output)
