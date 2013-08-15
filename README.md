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
    * use global configuration file (/etc/myproject/project.conf)
    * example of basic views and forms
    * basic use of dajax and dajaxice

The goal is also to provide many useful extra commands for distribute. Here is a list of commands I want to write:

  * generate API index file for Sphinx (done)
  * generate doc through Sphinx (done)
  * generate Pylint report (done)
  * compute dependencies thanks to snake food (done)
  * make i18n messages (done)
  * compile i18n messages (done)
  * generate pseudo-l10n files (done)
  * create a DMG on Mac OS X
  * test documentation (done)

I also want to provide templates for other classical Python programs:

  * Django application
  * Curse application
  * PyQt applications
  * daemon

Bento or distribute
