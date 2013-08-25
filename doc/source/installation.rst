Installing / Upgrading
======================

Installing from source
----------------------

If you prefer install directly from the source::

  $ cd StarterPyth
  $ sudo python setup.py install

You can also install _via_ pip::

  $ pip install starterpyth --user

Then you can call it through `starterpyth-bin`::

  $ starterpyth-bin


Creating packages
-----------------

You can easily create packages::

  $ cd StarterPyth
  $ python setup.py sdist # generate source .tar.gz file
  $ python setup.py bdist_deb  # require python-all and python-stdeb Debian packages
  $ python setup.py bdist_rpm
  $ python setup.py bdist_msi # generate a Windows installer
  $ python setup.py bdist # generate a binary .tar.gz


Generating documentation
------------------------

Documentation can be build thanks to sphinx doc generator::

  $ python setup.py gen_doc -html # generate HTML documentation (in doc/build/html)
  $ python setup.py gen_doc -latexpdf # generate PDF documentation (in doc/build/latex)
  $ python setup.py gen_doc -man # generate manual pages (in doc/build/man)
