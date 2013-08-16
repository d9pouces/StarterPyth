Quick tutorial and examples
===========================

Here is a simple example to create an empty Python module, named `Project`::

   $ starterpyth-bin
    Project name [default=Project]:
    Python module name [default=project]:
    Company name [default=19pouces.net]:
    Author name [default=d9pouces]: d9pouces
    Author e-mail [default=d9pouces@19pouces.net]:
    License [default=cecill b]:
    Minimum Python version [default=2.7]:
    Use six tool for Python 3 compatibility [default=yes]:
    Initial version [default=0.1]:
    Create a Django website [default=yes]:
    Create sample REST API with Tastypie [default=yes]:
    Create API doc with Tastypie Swagger [default=yes]:
    Create a shell application [default=yes]:
    Create a Cython application [default=yes]:

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
      compilemessages   Compile message files for i18n
      makemessages      Generate message files for i18n
      pseudo_l10n       Compile message files for i18n
      gen_doc_api       Generate simple API index for Sphinx documentation
      gen_doc           Compile project documentation
      test              run unit tests after in-place build
      profiling         Provide shortcuts for debugging and profiling functions
      lint              Evaluate code quality through pylint
      dependencies      Display a list of found dependencies
      doctest           Run examples provided in docstrings

    usage: setup.py [global_opts] cmd1 [cmd1_opts] [cmd2 [cmd2_opts] ...]
       or: setup.py --help [cmd1 cmd2 ...]
       or: setup.py --help-commands
       or: setup.py cmd --help


You should take a look to the documentation of plugins you want to use in :mod:`starterpyth.plugins`.
Provided commands are documentated in :mod:`starterpyth.commands`.
