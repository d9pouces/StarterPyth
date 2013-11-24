"""
Define input fields for command-line interface.
"""
import re
import six
import starterpyth.core
from starterpyth.log import yellow, red

from starterpyth.translation import ugettext as _

__author__ = 'd9pouces'


class ValidationError(ValueError):
    def __init__(self, msg):
        self.msg = msg
        super(ValidationError, self).__init__()


class BaseInput(object):
    def __init__(self, label, default=None):
        self.label = label
        self.default = default

    def validator(self, value):
        pass

    def convert_value(self, value):
        return value

    def input(self):
        prompt = _('%(label)s:') % {'label': self.label}
        if self.default is not None:
            prompt = _('%(label)s [default=%(default)s]: ') % {'label': self.label, 'default': self.default}
        valid = False
        value = ''
        while not valid:
            if starterpyth.core.INTERACTIVE:
                value = six.moves.input(prompt)
                if isinstance(value, six.binary_type):
                    value = value.decode('utf-8')
            else:
                value = self.default
                print(yellow(prompt + value))
            if not value and self.default is not None:
                value = self.default
            try:
                self.validator(value)
                valid = True
            except ValidationError as exception:
                print(red(exception.msg))
        value = self.convert_value(value=value)
        return value


class CharInput(BaseInput):
    def __init__(self, label, max_length, blank=True, default=None):
        self.max_length = int(max_length)
        self.blank = bool(blank)
        super(CharInput, self).__init__(label, default=default)

    def validator(self, value):
        if len(value) > self.max_length:
            raise ValidationError(_('Error: Maximum length for value is %(max_length)d') % {'max_length':
                                                                                            self.max_length})
        if not self.blank and not value:
            raise ValidationError(_('Error: Empty values are not allowed'))


class RegexpInput(BaseInput):
    def __init__(self, label, regexp, default=None):
        self.regexp = re.compile(regexp)
        super(RegexpInput, self).__init__(label, default=default)

    def validator(self, value):
        if not self.regexp.match(value):
            raise ValidationError(_('Error: Value must match the regexp %(regexp)s') % {'regexp': self.regexp.pattern})


class ChoiceInput(BaseInput):
    def __init__(self, label, choices, blank=False, default=None):
        self.choices = dict(choices)
        self.blank = blank
        super(ChoiceInput, self).__init__(label, default=default)

    def validator(self, value):
        if value not in self.choices:
            raise ValidationError(_('Error: Value must be one of %(choices)s') %
                                  {'choices': _(', ').join(self.choices.keys())})

    def convert_value(self, value):
        return self.choices[value]


class BooleanInput(BaseInput):
    def __init__(self, label, default=True):
        self.yes_str = _('yes')
        self.no_str = _('no')
        super(BooleanInput, self).__init__(label, default=self.yes_str if default else self.no_str)

    def validator(self, value):
        result = value.lower()
        if result not in (self.yes_str, self.no_str):
            raise ValidationError(_('Error: Value must be %(yes)s of %(no)s') %
                                  {'yes': self.yes_str, 'no': self.no_str})

    def convert_value(self, value):
        return value.lower() == self.yes_str
