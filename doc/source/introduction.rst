Introduction
============

Even after several years of Python programming, it seems hard to create *from scratch* a
well-structured project. :mod:`starterpyth` provides some help to create such a
project.

If everyone has different criterion to qualify a project as 'well-written'.
However, we can isolate some obvious ones.

    * follow Python guidelines,
    * follow common guidelines of the current OS,
    * respect a given coding style (e.g., PEP008),
    * provide a documentation (often in HTML) with examples,
    * pass unitary tests,
    * easy translation in different languages,
    * be easily distributed and installed.

These different steps can be achieved using :mod:`starterpyth`::

    $ starterpyth-bin
        > A small, valid Python project is generated, with examples of code and documentation
        [add your code and tests]
    $ python setup.py lint
        > Generate a report about the code quality
    $ python setup.py test
        > Run unitary tests
    $ python setup.py test_doc
        > Test examples provided in doc strings
    $ python setup.py gen_doc_api
        > Generate the index of your module API
    $ python setup.py gen_doc --html
        > Generate the documentation
    $ python setup.py makemessages
        > Prepare files for translation
        [translate .po files]
    $ python setup.py compilemessages
        > Compile translated files
    $ python setup.py bdist
        > Package your project into a .tar.gz file with binaries
    $ python setup.py sdist
        > Create a source package
