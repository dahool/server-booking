# -*- coding: utf-8 -*-
"""Copyright (c) 2011, Sergio Gabriel Teves
All rights reserved.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
import inspect

from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe

class Command(object):
    
    def __init__(self, name, label, can_get = False):
        self.name = name
        self.label = label
        if can_get:
            self.get_method = "get_%s" % name
            self.set_method = "set_%s" % name
        else:
            self.get_method = None
            self.set_method = name

    def set_console(self, console):
        self.console = console
        
    def _do_get(self):
        func = getattr(self.console, self.get_method)
        return func()
    
    def _do_set(self):
        pass
        
    value = property(_do_get, _do_set)
    
class RconCommands(object):
    
    def __init__(self, console):
        self.console = console
        self._init_commands()
    
    def _init_commands(self):
        self.commands = {}
        self.commands['map'] = Command('map', _('Map'), True)
        self.commands['nextmap'] = Command('nextmap', _('Next Map'), True)
        self.commands['password'] = Command('password', _('Password'), True)
        self.commands['gametype'] = Command('gametype', _('Game Type'), True)
        self.commands['cvar'] = Command('cvar', _('Cvar'), True)
        self.commands['write'] = Command('write', _('Write to console'))
        self.commands['cyclemap'] = Command('cyclemap', _('Cycle Map'))
        self.commands['restartmap'] = Command('restartmap', _('Restart Map'))
        self.commands['reloadmap'] = Command('reloadmap', _('Reload Map'))
        self.commands['bigtext'] = Command('bigtext', _('Bigtext'))
        self.commands['say'] = Command('say', _('Say'))
        self.commands['kick'] = Command('kick', _('Kick'))
        self.commands['slap'] = Command('slap', _('Slap'))
        
    def _call(self, func, *args):
        if self._use_args(func):
            return func(*args)
        return func()
        
    def _use_args(self, func):
        if len(inspect.getargspec(func).args) > 1:
            return True
        return False

    def get_command(self, cmd):
        return self.commands[cmd]
    
    def set(self, cmd_name, *args):
        command = self.commands[cmd_name]
        func = getattr(self.console, command.set_method)
        return self._call(func, *args)
        
    def get(self, cmd_name, *args):
        command = self.commands[cmd_name]
        if command.get_method:
            func = getattr(self.console, command.get_method)
            return self._call(func, *args)
        raise NotImplementedError()
    
    @property
    def as_html(self):
        html = "<table>"
        for name,cmd in self.commands.items():
            html += '<tr><td>%s&nbsp;:&nbsp;' % cmd.label
            func = getattr(self.console, cmd.set_method)
            if self._use_args(func):
                html += '<input type="text" name="%s">' % name
            if cmd.get_method:
                html += '<input type="button" class="command_get green" alt="%s" value="%s">' % (name, _('Get'))
            html += '<input type="button" class="command_set red" alt="%s" value="%s">' % (name, _('Set'))
            html += '</td></tr>'
        html += '</table>'
        return mark_safe(html)