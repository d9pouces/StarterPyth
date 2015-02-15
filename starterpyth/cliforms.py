#coding=utf-8
import os
import re

from six import PY2

from starterpyth.log import display, RED
from starterpyth.translation import ugettext as _


__author__ = 'flanker'


# noinspection PyUnresolvedReferences
input_ = raw_input if PY2 else input


class InvalidValue(ValueError):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class Input(object):
    __ORDER = 0

    def __init__(self, label='', initial=None, show=None):
        self.show = show
        self.label = label
        self.initial = initial
        self.order = Input.__ORDER
        Input.__ORDER += 1

    def read(self, initial=None):
        if initial is None:
            initial = self.initial
        raw_value = input_(self.widget(initial=initial))
        if not raw_value and initial is not None:
            raw_value = self.to_str(initial)
        while True:
            try:
                valid_value = self.to_python(raw_value)
                break
            except InvalidValue as e:
                display(_('Invalid value: %(value)s (%(msg)s)') % {'value': raw_value, 'msg': str(e)}, color=RED,
                        bold=True)
                raw_value = input_(self.widget())
                if not raw_value and initial is not None:
                    raw_value = self.to_str(initial)
        # noinspection PyUnboundLocalVariable
        return valid_value

    def widget(self, initial=None):
        raise NotImplementedError

    def to_str(self, value):
        raise NotImplementedError

    def to_python(self, value):
        raise NotImplementedError


class CharInput(Input):

    def __init__(self, label='', initial=None, max_length=None, min_length=None, show=None):
        super(CharInput, self).__init__(label=label, initial=initial, show=show)
        self.max_length = max_length
        self.min_length = min_length

    def widget(self, initial=None):
        if initial:
            return _('%(label)s [%(init)s]: ') % {'label': self.label, 'init': self.to_str(initial)}
        else:
            return _('%(label)s: ') % {'label': self.label}

    def to_str(self, value):
        return str(value)

    def to_python(self, value):
        if self.min_length is not None and self.min_length > len(value):
            raise InvalidValue(_('Value must be at least %(l)d character long') % {'l': self.min_length})
        if self.max_length is not None and self.max_length < len(value):
            raise InvalidValue(_('Value must be at most %(l)d character long') % {'l': self.max_length})
        return value


class RegexpInput(CharInput):
    def __init__(self, regexp, label='', initial=None, show=None):
        super(RegexpInput, self).__init__(label=label, initial=initial, show=show)
        self.regexp = regexp

    def to_python(self, value):
        if not self.regexp.match(value):
            raise InvalidValue(_('Value must match %(l)s regexp') % {'l': self.regexp.pattern})
        return value


class IntegerInput(RegexpInput):
    def __init__(self, min_value=None, max_value=None, label='', initial=None, required=True, show=None):
        super(IntegerInput, self).__init__(re.compile('\d+'), label=label, initial=initial, show=show)
        self.max_value = max_value
        self.min_value = min_value
        self.required = required

    def to_python(self, value):
        if not self.required and not value:
            return None
        if not self.regexp.match(value):
            raise InvalidValue(_('Value must be a integer'))
        value = int(value)
        if self.min_value is not None and self.min_value > value:
            raise InvalidValue(_('Value must be greater than %(l)d ') % {'l': self.min_value})
        if self.max_value is not None and self.max_value < value:
            raise InvalidValue(_('Value must be less than %(l)d') % {'l': self.max_value})
        return value


class BooleanInput(CharInput):
    true_values = [_('yes'), _('y')]
    false_values = [_('no'), _('n')]

    def to_python(self, value):
        value = value.lower()
        if value in self.true_values:
            return True
        elif value in self.false_values:
            return False
        raise InvalidValue(_('Value must be one of %(l)s') % {'l': ', '.join(self.true_values + self.false_values)})

    def to_str(self, value):
        if value:
            return self.true_values[0]
        return self.false_values[0]

    def widget(self, initial=None):
        if initial is None:
            choices = _('%s/%s') % (self.true_values[0], self.false_values[0])
        elif initial:
            choices = _('%s/%s') % (self.true_values[0].upper(), self.false_values[0])
        else:
            choices = _('%s/%s') % (self.true_values[0], self.false_values[0].upper())
        return _('%(label)s [%(choices)s]: ') % {'label': self.label, 'choices': choices}


class PathInput(CharInput):
    def __init__(self, cwd=None, label='', initial=None, required=True, show=None):
        super(PathInput, self).__init__(label=label, initial=initial, show=show)
        self.cwd = cwd
        self.required = required

    def to_python(self, value):
        if not value and self.required:
            raise InvalidValue(_('Please enter a valid path'))
        elif not value:
            return None
        if self.cwd:
            value = os.path.join(self.cwd, value)
        if not os.path.exists(value):
            raise InvalidValue(_('%(l)s is not a valid path') % {'l': value})
        return value


class ChoiceInput(CharInput):
    int_re = re.compile(r'\d+')

    def __init__(self, choices, label='', initial=None, required=True, show=None):
        super(ChoiceInput, self).__init__(label=label, initial=initial, show=show)
        if hasattr(choices, '__call__'):
            choices = choices()
        self.choices = choices
        self.required = required

    def to_python(self, value):
        if not value and self.required:
            raise InvalidValue(_('Please enter a valid choice'))
        elif not value:
            return None
        if not self.int_re.match(value) or not (1 <= int(value) <= len(self.choices)):
            raise InvalidValue(_('Please enter a number between 1 and %(max)d') % {'max': len(self.choices)})
        return self.choices[int(value) - 1][0]

    def display(self, value):
        return self.choices[int(value) - 1][1]

    def widget(self, initial=None):
        def l(i, x):
            if initial is not None and x[0] == initial:
                return _('    [%d] %s') % (i + 1, x[1])
            return _('    %d %s') % (i + 1, x[1])
        choices = _('\n').join([l(i, x) for (i, x) in enumerate(self.choices)])
        return _('%(label)s:\n%(choices)s\n    ') % {'label': self.label, 'choices': choices}

    def to_str(self, value):
        for i, (k, v) in enumerate(self.choices):
            if value == k:
                return str(i + 1)
        return ''


class BaseForm(object):

    def __init__(self, initial=None):
        super(BaseForm, self).__init__()
        self.initial = {} if initial is None else initial

    def read(self, interactive=True):
        fields = []
        for key, field in self.__class__.__dict__.items():
            if isinstance(field, Input):
                fields.append((key, field))
        fields.sort(key=lambda f_: f_[1].order)
        values = {}
        for key, field in fields:
            kwargs = {}
            show = field.show
            init_value = self.initial.get(key, field.initial)
            if hasattr(init_value, '__call__') and not isinstance(init_value, type):
                init_value = init_value(**values)
            if show is not None:
                if hasattr(show, '__call__'):
                    show = show(**values)
                if not show:
                    values[key] = init_value
                    continue
            kwargs['initial'] = init_value
            if interactive:
                values[key] = field.read(**kwargs)
            else:
                values[key] = kwargs.get('initial', field.initial)
        return values


if __name__ == '__main__':
    import doctest

    doctest.testmod()