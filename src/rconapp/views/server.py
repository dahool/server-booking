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

from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.http import HttpResponseRedirect
from django.views.decorators.cache import cache_page
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic.list_detail import object_detail, object_list
from django.shortcuts import get_object_or_404

from common.view.decorators import render
from common.decorators import superuser_required, permission_required_with_403
from common.middleware.exceptions import Http403

from rconapp.models import Server
from rconapp.forms import ServerForm

# server.can_add ??
#@permission_required_with_403('rconapp.add_server')
@render('rconapp/server_form.html')
def server_create_update(request, slug=None):
    res = {}
    if request.method == 'POST':
        if slug:
            s = get_object_or_404(Server, slug=slug)
            res['server']=s
            form = ServerForm(request.POST, instance=s)
        else:
            form = ServerForm(request.POST)
        if form.is_valid():
            s = form.save(True)
            return HttpResponseRedirect(s.get_absolute_url())
        res['form'] = form
    else:
        if slug:
            s = get_object_or_404(Server, slug=slug)
            res['server']=s
            form = ServerForm(instance=s)
        else:
            form = ServerForm(initial={'password': ''})
        res['form'] = form 
    return res

#@permission_required_with_403('rconapp.delete_server')
def server_delete(request, slug=None):
    '''
    projects can be deleted by staff members only
    '''
    p = get_object_or_404(Server, slug=slug)
    p.delete()
    return HttpResponseRedirect(reverse('server_list'))

#@login_required
def server_detail(request, slug):
    return object_detail(request,
                         queryset=Server.objects.all(),
                         template_object_name= 'server',
                         slug=slug)
        
#@login_required
@cache_page(60)
@render('rconapp/server_list.html')
def server_list(request):
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    paginator = Paginator(Server.objects.all(), settings.SERVERS_PER_PAGE)
    try:
        list = paginator.page(page)
    except (EmptyPage, InvalidPage):
        list = paginator.page(paginator.num_pages)
        
    return {'servers': list}