# -*- coding: utf-8 -*-
import copy
from errno import ENOENT
import gettext as gettext_module
import os.path
import pkg_resources

__all__ = ['translation', 'gettext', 'lgettext', 'ugettext', 'ngettext', 'lngettext', 'ungettext']


# Locate a .mo file using the gettext strategy
def __find(domain, locale_module, localedir='locale', languages=None):
    """
    Return the name of a .mo file using the gettext strategy.

    :param domain: Gettext domain name (e.g. your module name)
    :param localedir: directory containing locales (give 'locale' if you have locale/fr_FR/LC_MESSAGES/domain.mo)
    :param languages: languages to find (if None: calculated with LANGUAGE, LC_ALL, LC_MESSAGES, LANG env. variables)
    """
    # Get some reasonable defaults for arguments that were not supplied
    if languages is None:
        languages = []
        for envar in ('LANGUAGE', 'LC_ALL', 'LC_MESSAGES', 'LANG'):
            val = os.environ.get(envar)
            if val:
                languages = val.split(':')
                break
        if 'C' not in languages:
            languages.append('C')
    # now normalize and expand the languages
    nelangs = []
    for lang in languages:
        # noinspection PyProtectedMember
        for nelang in gettext_module._expand_lang(lang):  # pylint: disable=W0212
            if nelang not in nelangs:
                nelangs.append(nelang)
    # select a language
    result = []
    for lang in nelangs:
        if lang == 'C':
            break
        mofile = '%s/%s/%s/%s.mo' % (localedir, lang, 'LC_MESSAGES', domain)
        if pkg_resources.resource_exists(locale_module, mofile):
            result.append(mofile)
    return result


def translation(domain, locale_module, localedir='locale', languages=None, class_=None, fallback=False):
    """

    :param domain:
    :param localedir:
    :param languages:
    :param class_:
    :param fallback:
    :return: :raise:
    """
    if class_ is None:
        class_ = gettext_module.GNUTranslations
    mofiles = __find(domain, locale_module, localedir, languages)
    if not mofiles:
        if fallback:
            return gettext_module.NullTranslations()
        raise IOError(ENOENT, 'No translation file found for domain', domain)
    # Avoid opening, reading, and parsing the .mo file after it's been done once.
    result = None
    if mofiles is not None:
        for mofile in mofiles:
            key = (class_, mofile)
            # noinspection PyProtectedMember
            trans_obj = gettext_module._translations.get(key)  # pylint: disable=W0212
            if trans_obj is None:
                with pkg_resources.resource_stream(locale_module, mofile) as fileobj:
                    # noinspection PyProtectedMember
                    trans_obj = gettext_module._translations.setdefault(key, class_(fileobj))  # pylint: disable=W0212
            # Copy the translation object to allow setting fallbacks and
            # output charset. All other instance data is shared with the
            # cached object.
            trans_obj = copy.copy(trans_obj)
            if result is None:
                result = trans_obj
            else:
                result.add_fallback(trans_obj)
    return result


parent_package = os.path.basename(os.path.dirname(__file__))

__TRANS = translation(parent_package, parent_package, fallback=True)
# pylint: disable=C0103
gettext = __TRANS.gettext
lgettext = __TRANS.lgettext
ngettext = __TRANS.ngettext
lngettext = __TRANS.lngettext
ugettext = __TRANS.gettext
ungettext = __TRANS.ngettext
if hasattr(__TRANS, 'ugettext'):
    ugettext = getattr(__TRANS, 'ugettext')
if hasattr(__TRANS, 'ungettext'):
    ungettext = getattr(__TRANS, 'ungettext')
