#coding=utf-8
from starterpyth.cliforms import BaseForm, CharInput, BooleanInput

__author__ = 'flanker'


class TestForm(BaseForm):
    c_323 = CharInput(label='label1', min_length=12)
    c_2 = CharInput(label='label2', initial='42')
    tru0 = BooleanInput(label='test bool')
    tru1 = BooleanInput(label='test bool', initial=True)
    tru2 = BooleanInput(label='test bool', initial=False)


if __name__ == '__main__':

    form = TestForm()
    values = form.read()
    print(values)

    import doctest

    doctest.testmod()