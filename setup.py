import codecs
import logging
import os.path

from setuptools import setup, find_packages

from starterpyth.log import CONSOLE, dict_config

__author__ = 'd9pouces'

dict_config(CONSOLE)

# noinspection PyUnresolvedReferences
if os.path.isdir(os.path.join(os.path.dirname(__file__), '.git')):
    try:
        import setuptools_git
    except ImportError:
        setuptools_git = None
        logging.warning('You should install setuptools-git to track data files.')

readme = os.path.join(os.path.dirname(__file__), 'README.md')
if os.path.isfile(readme):
    fd = codecs.open(readme, 'r', encoding='utf-8')
    long_description = fd.read()
    fd.close()
else:
    long_description = ''

setup(
    name='starterpyth',
    version='0.5.2',
    description='Generate good skeletons of Python applications.',
    long_description=long_description,
    author='d9pouces',
    author_email='d9pouces@19pouces.net',
    license='Cecill-B',
    url='http://www.19pouces.net/projects.html',
    entry_points={
        'console_scripts': [
            'starterpyth-bin = starterpyth.core:main',
        ],
        "distutils.commands": [
            "dependencies = starterpyth.commands.dependencies:Dependencies",
            "profiling = starterpyth.commands.profiling:Profiling",
            "lint = starterpyth.commands.lint:Lint",
            "gen_doc = starterpyth.commands.gen_doc:GenDoc",
            "makemessages = starterpyth.commands.makemessages:MakeMessages",
            "compilemessages = starterpyth.commands.compilemessages:CompileMessages",
            "doctest = starterpyth.commands.doc_test:DocTest",
            "gen_doc_api = starterpyth.commands.gen_doc_api:GenDocApi",
            "pseudo_l10n = starterpyth.commands.pseudo_l10n:PseudoL10N",
        ],
    },
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    test_suite='starterpyth.tests',
    use_2to3=True,
    convert_2to3_doctests=['src/your/module/README.txt'],
    use_2to3_fixers=[],
    use_2to3_exclude_fixers=[],
    # extra_requires=['pylint', 'sphinx'],
    install_requires=['distribute', 'jinja2', 'markupsafe', ],
    setup_requires=['distribute'],
)
