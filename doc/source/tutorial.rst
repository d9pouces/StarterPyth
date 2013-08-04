Quick tutorial and examples
===========================

Here is a simple example to create an empty Python module, named `Project`::

   $ starterpyth-bin
   Please enter a name for your project [Test]: Project
   Please enter a name for your main Python module [project]: 
   Author name [flanker]:
   Version [0.1]: 
   Please enter a short description []: 
   Licence [Cecill-B]: 
   Author email [flanker@19pouces.net]:
   [Using plugin BaseApp]:
   Copying README.txt
   Copying notes.txt
   Copying MANIFEST.in
   Copying stdeb.cfg
   Copying setup.py
   Copying setup.cfg
   Copying test/__init__.py
   Copying test/utils.py
   Copying test/data/README
   Copying doc/make.bat
   Copying doc/Makefile
   Copying doc/source/tutorial.rst
   Copying doc/source/conf.py
   Copying doc/source/index.rst
   Copying doc/source/installation.rst
   [Using plugin ShellApp]:
   Are you writing a shell script? [yes]: no
   [Using plugin QtApp]:
   Are you writing a Qt application? [yes]: no
   [Using plugin DjangoApp]:
   Are you writing a Django website? [yes]: no
   [Using plugin Setup]:
   Copying setup.py

A new directory is created `Project`, containing all files required to cleanly
develop, test, distribute and install the project.

The generated setup.py file provides many interesting commands::

    $ cd Project
    $ python setup.py --help-commands
    Standard commands:
      clean             clean up temporary files from 'build' command
      install           install everything from build directory
      sdist             create a source distribution (tarball, zip file, etc.)
      bdist             create a built (binary) distribution
      bdist_rpm         create an RPM distribution
      check             perform some checks on the package
    
    Extra commands:
      gen_doc_api       Generate simple API index for Sphinx documentation
      gen_doc           Compile project documentation
      test              run unit tests after in-place build
      lint              Evaluate code quality through pylint
      dependencies      Display a list of found dependencies
      bdist_deb         distutils command to create debian binary package
      test_doc          Run examples provided in docstrings
      makemessages      Create translation files
      compilemessages   Compile translation files

    usage: setup.py [global_opts] cmd1 [cmd1_opts] [cmd2 [cmd2_opts] ...]
       or: setup.py --help [cmd1 cmd2 ...]
       or: setup.py --help-commands
       or: setup.py cmd --help


You should take a look to the documentation of plugins you want to use in :mod:`starterpyth.plugins`.
Provided commands are documentated in :mod:`starterpyth.command`.
