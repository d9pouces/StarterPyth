from starterpyth.log import green, yellow, red

__author__ = 'd9pouces'
import os
import shlex
import shutil
import subprocess

from distutils.core import Command

try:
    #noinspection PyPackageRequirements
    import sphinx
except ImportError:
    sphinx = None

from starterpyth.translation import gettext as _


class GenDoc(Command):
    ALLSPHINXOPTS = '-d %s/doctrees -D latex_paper_size=a4 %s %s'

    description = 'Compile project documentation'

    user_options = [
        ('doc-dir=', None, "documentation root"),
        ('build-dir=', 'b', "build directory"),
        ('clean', None, "remove existing files"),
        ('html', None, 'to make standalone HTML files'),
        ('dirhtml', None, 'to make HTML files named index.html in directories'),
        ('singlehtml', None, 'to make a single large HTML file'),
        ('pickle', None, 'to make pickle files'),
        ('json', None, 'to make JSON files'),
        ('htmlhelp', None, 'to make HTML files and a HTML help project'),
        ('epub', None, 'to make an epub'),
        ('latex', None, 'to make LaTeX files, you can set PAPER=a4 or PAPER=letter'),
        ('latexpdf', None, 'to make LaTeX files and run them through pdflatex'),
        ('text', None, 'to make text files'),
        ('man', None, 'to make manual pages'),
        ('changes', None, 'to make an overview of all changed/added/deprecated items'),
        ('linkcheck', None, 'to check all external links for integrity'),
        ('doctest', None, 'to run all doctests embedded in the documentation (if enabled)'),
    ]
    outputs = {'html': "Build finished. The HTML pages are in %s/html.",
               'dirhtml': "Build finished. The HTML pages are in %s/dirhtml.",
               'singlehtml': "Build finished. The HTML page is in %s/singlehtml.",
               'pickle': "Build finished; now you can process the pickle files.",
               'json': "Build finished; now you can process the JSON files.",
               'htmlhelp': "Build finished; now you can run HTML Help Workshop with the \n ."
                           "hhp project file in %s/htmlhelp.",
               'epub': "Build finished. The epub file is in %s/epub.",
               'latex': "Build finished; the LaTeX files are in %s/latex.",
               'latexpdf': "Running LaTeX files through pdflatex in %s/latex...",
               'text': "Build finished. The text files are in %s/text.",
               'man': "Build finished. The manual pages are in %s/man.",
               'changes': "The overview file is in %s/changes.",
               'linkcheck': "Link check complete; look for any errors in the above output \n "
                            "or in %s/linkcheck/output.txt.",
               'doctest': "results in %s/doctest/output.txt.", }

    def __init__(self, *args, **kwargs):
        Command.__init__(self, *args, **kwargs)
        self.doc_dir = 'doc/source'
        self.build_dir = 'doc/build'
        self.clean = 0
        self.html = None
        self.dirhtml = None
        self.singlehtml = None
        self.pickle = None
        self.json = None
        self.htmlhelp = None
        self.epub = None
        self.latex = None
        self.latexpdf = None
        self.text = None
        self.man = None
        self.changes = None
        self.linkcheck = None
        self.doctest = None

    def initialize_options(self):
        pass

    def finalize_options(self):
        self.build_dir = os.path.abspath(self.build_dir)
        self.doc_dir = os.path.abspath(self.doc_dir)

    def run(self):
        if sphinx is None:
            print(red(_('package sphinx is required.')))
            return 1
        if self.clean and os.path.isdir(self.build_dir):
            msg = _('removing %(dir)s') % {'dir': self.build_dir}
            print(green(msg))
            shutil.rmtree(self.build_dir)
        sphinx_opts = shlex.split(self.ALLSPHINXOPTS % (self.build_dir, os.getenv('SPHINXOPTS') or '', self.doc_dir))
        count = 0
        for orig_fmt, txt in self.outputs.items():
            fmt = 'latex' if orig_fmt == 'latexpdf' else orig_fmt
            if orig_fmt not in self.distribution.command_options['gen_doc']:
                continue
            count = 1
            options = ['sphinx-build', '-b', fmt, ] + sphinx_opts + [os.path.join(self.build_dir, fmt), ]
            result = sphinx.main(options)
            if result == 0:
                msg = txt % self.build_dir
                print(green(msg))
                if orig_fmt == 'latexpdf':
                    subprocess.check_call('make -C %s/latex all-pdf' % self.build_dir, shell=True)
                    msg = "pdflatex finished; the PDF files are in %s/latex." % self.build_dir
                    print(green(msg))
        if not count:
            print(yellow(_("please select at least one output format (e.g. gen_doc --html)")))
