import codecs
import os.path
from setuptools import setup, find_packages
from starterpyth import __version__ as version
__author__ = 'd9pouces'


# get README content from README.rst file
readme = os.path.join(os.path.dirname(__file__), 'README.rst')
fd = codecs.open(readme, 'r', encoding='utf-8')
long_description = fd.read()
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
    entry_points={'console_scripts': ['starterpyth-bin = starterpyth.core:main', ], },
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    test_suite='starterpyth.tests',
    use_2to3=False,
    install_requires=['setuptools>=0.7', 'jinja2', 'markupsafe', 'six', ],
    setup_requires=['setuptools>=0.7', ],
)
