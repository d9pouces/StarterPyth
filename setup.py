import codecs
import os.path
from setuptools import setup, find_packages
from starterpyth import __version__ as version

__author__ = 'Matthieu Gallet'


# get README content from README.rst file
readme = os.path.join(os.path.dirname(__file__), 'README.rst')
fd = codecs.open(readme, 'r', encoding='utf-8')
long_description = fd.read()
fd.close()

SETUP_COMMANDS = [
    ('CompileMessages', 'compilemessages',),
    ('Dependencies', 'dependencies',),
    ('DocTest', 'doc_test',),
    ('GenDoc', 'gen_doc',),
    ('GenDocApi', 'gen_doc_api',),
    ('Lint', 'lint'),
    ('MakeMessages', 'makemessages',),
    ('Profiling', 'profiling'),
]
extra_requires = {'all': ['sfood', 'pylint', 'pstats', ], }

setup(
    name='starterpyth',
    version=version,
    description='Generate skeletons for new Python applications.',
    long_description=long_description,
    author='Matthieu Gallet',
    author_email='Matthieu Gallet@19pouces.net',
    license='Cecill-B',
    url='http://www.19pouces.net/projects.html',
    entry_points={'console_scripts': ['starterpyth-bin = starterpyth.core:main', ],
                  'distutils.commands': ["%(cmd)s = starterpyth.commands.%(cmd)s:%(cls)s" % {'cmd': data[1], 'cls': data[0]}
                                         for data in SETUP_COMMANDS],
                  },
    packages=find_packages(),
    include_package_data=True,
    extra_requires=extra_requires,
    zip_safe=True,
    test_suite='starterpyth.tests',
    use_2to3=False,
    install_requires=['setuptools>=0.7', 'jinja2', 'markupsafe', 'six', ],
    setup_requires=['setuptools>=0.7', ],
)
