StarterPyth
===========

Generate good skeletons of Python applications.

Creating a new Python program require a lot of work: preparing the setup.py file, initial translation files, ...

StarterPyth aims at doing this for you. Just choose your type of application, and you get a functionnal starting point.
You only have to write original code, not starting by copying the same code again and again.

You can decide to create different kinds of Python applications:

  * plain-Python package
  * command-line application
  * Cython-based extension
  * Django-based website with custom commands and optional modules

    * create basic configurations for nginx and Apache
    * examples of tastypie REST APIs
    * example of basic views and forms
    * use global configuration file (/etc/myproject/project.conf) [TODO]
    * basic use of dajax and dajaxice [TODO]

The goal is also to provide many useful extra commands for distribute. Here is a list of commands I want to write:

  * generate API index file for Sphinx
  * generate doc through Sphinx
  * generate Pylint report
  * compute dependencies thanks to snake food
  * make i18n messages
  * compile i18n messages
  * generate pseudo-l10n files
  * test documentation

I also want to provide templates for other classical Python programs:

  * Django application
  * Curse application
  * PyQt applications
  * daemon

You can install it with pip::

    $ pip install starterpyth

...or from the source::

    $ cd StarterPyth
    $ sudo python setup.py install


Then you can call it through `starterpyth-bin`::

    $ starterpyth-bin


More complete documentation can be found at https://starterpyth.readthedocs.org/en/latest/


Starterpyth 2.0 :
    doctest, unittest, nose
    mock
    pychecker, pylint, pyflakes
    * CHANGES.txt

    * CLI
        * man page

    * Django
        * passer à DjangoFloor 0.9
        * configuration sentry

    * démon -> fichiers de conf pour launchd / systemd

    * utilisation de six
    * création de l'environnement virtuel associé
    * template PyCharm [avec environnement virtuel, warning sur la version de Python]
    * intégration avec tox, github, travis, readthedocs
