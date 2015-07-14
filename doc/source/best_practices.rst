Best practices of Python programming
====================================


Directory structure
~~~~~~~~~~~~~~~~~~~

First of all, the general organization of your project should be like the following one::


    MyProjectName/
    |-- README, README.md, README.rst, or README.txt
    |-- LICENSE
    |-- setup.py
    |-- MyPythonPackage/
    |   |-- __init__.py
    |   |-- useful_1.py
    |   |-- useful_2.py
    |   |-- locale/
    |   |   |-- fr_FR/
    |   |   |   \-- LC_MESSAGES/
    |   |   |       |-- MyPythonPackage.mo
    |   |   |       \-- MyPythonPackage.po
    |   |   \-- MyPythonPackage.pot
    |   \-- tests/
    |       |-- __init__.py
    |   	|-- test_useful_1.py
    |   	\-- test_useful_2.py
    \-- doc
        |-- source/
        |   |-- index.rst
        |   \-- conf.py
        |-- build/
        |   |-- html/
        |   \-- pdf/
        |-- Makefile
        \-- make.bat


External tools
~~~~~~~~~~~~~~

Python comes with an extensive standard library, however, serveral external tools are still required to enhance your
programs. In a few words, here is the list of required tools:

  * `setuptools >= 1.0 <https://pypi.python.org/pypi/setuptools/1.1>`_,
  * `six <https://pypi.python.org/pypi/six/1.4.1>`_ or 2to3,
  * `pylint <https://pypi.python.org/pypi/pylint/1.0.0>`_,
  * `nose <http://nose.readthedocs.org/en/latest/>`_,



Packaging and distribution
^^^^^^^^^^^^^^^^^^^^^^^^^^

A good preview of the different ways to package a Python module is given on `stackoverflow <http://stackoverflow.com/questions/6344076/differences-between-distribute-distutils-setuptools-and-distutils2>`_.
The current best solution is to use `setuptools >= 1.0 <https://pypi.python.org/pypi/setuptools/1.1>`_.
Other solutions (including `distribute`, `distutils2`, `distlib`) are abandoned, the basic `distutils` lacks some features,
and `bento <http://cournape.github.io/Bento/>`_ is not mature yet.

Code quality
^^^^^^^^^^^^

`pylint <https://pypi.python.org/pypi/pylint/1.0.0>`_ is a Python source code analyzer. If `starterpyth` is also installed,
you can use `python setup.py lint` to check your code.


Testing
^^^^^^^

The standard library provide two frameworks for unitary tests: `unittest <http://docs.python.org/3/library/unittest.html>`_
and `doctest <http://docs.python.org/3/library/doctest.html#module-doctest>`_.

However, it can be improved by `nose <http://nose.readthedocs.org/en/latest/>`_, that can check for code coverage.


Documentation
^^^^^^^^^^^^^

Many projects are documented thanks to `Sphinx <http://sphinx-doc.org>`_. Starterpyth generate a skeleton of Sphinx
documentation.
You can create an index file of your complete API and then generate the whole documention with only two commands::

   $ python setup.py gen_doc_api
   $ python setup.py gen_doc --html

The first command generates a `.rst` file for each of your Python file in `source/api`. The second one generates the
documentation, as it can be done with `cd doc; make html`.

Python 2 and 3 compatibility
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

More informations are available on the official `Python documentation <http://docs.python.org/3/howto/pyporting.html>`_.
For simple projects, you can write Python 2/3 compatible code. For larger projects, you can use either the
`six <https://pypi.python.org/pypi/six/1.4.1>`_ tool, or
`2to3 <http://docs.python.org/3/howto/pyporting.html#use-2to3>`_.

Do not forget that requiring at least Python 2.6/7 (for the 2.x branch) and Python 3.2 (for the 3.x branch) can ease
your work. Supporting Python 3.0 can lead to a lot of work for a little advantage.
More and more libraries are compatible with Python 3.2+, so you should consider to work with Python 3 for new projects.


Virtual environments
^^^^^^^^^^^^^^^^^^^^

Coding conventions
^^^^^^^^^^^^^^^^^^

Most Python programmers follow the `PEP008 <http://www.python.org/dev/peps/pep-0008/>`_.