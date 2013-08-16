from starterpyth.fields import BooleanInput

__author__ = 'd9pouces'

from starterpyth.core import Plugin
from starterpyth.translation import ugettext as _


class CliPlugin(Plugin):

    def __init__(self):
        self.selected = True
        super(CliPlugin, self).__init__()

    def is_selected(self):
        return self.selected

    def update_global_context(self, context, filters):
        self.selected = BooleanInput(_('Create a shell application'), default=True).input()
        if not self.selected:
            return
        script = '%(module_name)s-bin = %(module_name)s.cli:main' % {'module_name': context['module_name']}
        context['entry_points'].setdefault('console_scripts', []).append(script)

    def get_resources(self):
        return 'starterpyth.plugins.cli', 'templates'
