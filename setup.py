import codecs
import os.path
import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages

__author__ = 'd9pouces'


# get README content from README.rst file
readme = os.path.join(os.path.dirname(__file__), 'README.rst')
fd = codecs.open(readme, 'r', encoding='utf-8')
long_description = fd.read()
fd.close()

# get version value from VERSION file
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
    entry_points={'console_scripts': ['starterpyth-bin = starterpyth.core:main', ], },
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    test_suite='starterpyth.tests',
    use_2to3=False,
    install_requires=['setuptools>=0.7', ],
    setup_requires=['setuptools>=0.7', 'jinja2', 'markupsafe', 'six', ],
)
