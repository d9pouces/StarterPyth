import codecs
import os.path
import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages

__author__ = 'd9pouces'

readme = os.path.join(os.path.dirname(__file__), 'README.rst')
if os.path.isfile(readme):
    fd = codecs.open(readme, 'r', encoding='utf-8')
    long_description = fd.read()
    fd.close()
else:
    long_description = ''

version_filename = os.path.join(os.path.dirname(__file__), 'VERSION')
fd = open(version_filename, 'r')
version = fd.read().strip()
fd.close()

setup(
    name='starterpyth',
    version=version,
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
    zip_safe=False,
    test_suite='starterpyth.tests',
    use_2to3=False,
    extra_requires=['polib', 'pylint', 'sphinx'],
    install_requires=['setuptools>=0.7', 'jinja2', 'markupsafe', 'six', ],
    setup_requires=['setuptools>=0.7'],
)
