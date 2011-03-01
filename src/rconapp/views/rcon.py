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

from django.views.decorators.cache import cache_page
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from common.view.decorators import render
from common.decorators import superuser_required, post_required
from common.middleware.exceptions import Http403

from q3console.urtconsole import UrtClient
from rconapp.models import Server
from rconapp.exceptions import ApplicationError
from rconapp.commands import RconCommands
from rconapp.functions import create_rcon_audit

class Status(object):
    gametype = ''
    map = ''

def _get_console(server, check = True):
    try:
        console = UrtClient(server.host, server.rconpassword)
    except:
        raise ApplicationError(_('Unable to contact server. Server down?'))

    if check:
        try:
            # use this instead of check to cache player list and avoid a second call to status
            console.get_player_list()
        except:
            raise ApplicationError(_('Bad rcon password'))
    
    return console

@render('rconapp/rcon/home.html')
def home(request, slug):
    server = get_object_or_404(Server, slug=slug)
    console = _get_console(server)
    status = Status()
    status.gametype =console.get_gametype()
    status.map = console.get_map()
    cmds = RconCommands(console)
    return {'server': server,
            'status': status,
            'commands': cmds}
    
@post_required
@render('rconapp/rcon/status.html')
def refresh_status(request, slug):
    server = get_object_or_404(Server, slug=slug)
    console = _get_console(server)
    status = Status()
    status.gametype =console.get_gametype()
    status.map = console.get_map()
    return {'server': server,
            'status': status}

@post_required
@cache_page(15)
@render('rconapp/rcon/clients.html')
def refresh_clients(request, slug):
    server = get_object_or_404(Server, slug=slug)
    console = _get_console(server)
    players = console.get_player_list()
    return {'server': server,
            'clients': players}
                    
@post_required
def execute(request, slug):
    server = get_object_or_404(Server, slug=slug)
    console = _get_console(server, False)

    command = request.POST.get('cmd')
    action = request.POST.get('action')
    data = request.POST.get('data')

    commands = RconCommands(console)
    cmd = commands.get_command(command).label
    
    # audit user action
    create_rcon_audit(request, server, '%s: %s %s' % (command, action, data))
    
    if action == 'get':
        r = commands.get(command, data)
        if data:
            res = '%s: %s = %s' % (cmd,data,r)  
        else:
            res = '%s: %s' % (cmd,r)
    elif action == 'set':
        r = commands.set(command, data)
        if not r:
            if data:
                res = _('Done %s %s' % (cmd, data))  
            else:
                res = _('Done %s' % (cmd))
        else:
            res = '%s: %s' % (cmd,r)  
    else:
        res = _('Unknown')
    return HttpResponse(res)