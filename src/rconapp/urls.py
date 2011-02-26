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

from django.conf.urls.defaults import *
from views import server as server_views
from views import rcon as rcon_views

# --- SERVER VIEWS --------
urlpatterns = patterns('',
    url(
        regex = '^add/$',
        view = server_views.server_create_update,
        name = 'server_create'),
    url(
        regex = '^(?P<slug>[-\w]+)/edit/$',
        view = server_views.server_create_update,
        name = 'server_edit',),
    url(
        regex = '^(?P<slug>[-\w]+)/delete/$',
        view = server_views.server_delete,
        name = 'server_delete',),
    url (
        regex = '^$',
        view = server_views.server_list,
        name = 'server_list'),   
) 
urlpatterns += patterns('django.views.generic',
    url(
        regex = '^(?P<slug>[-\w]+)/details/$',
        view = server_views.server_detail,
        name = 'server_detail'),
)

# --- RCON VIEWS --------
urlpatterns += patterns('',
    url(
        regex = '^(?P<slug>[-\w]+)/rcon/$',
        view = rcon_views.home,
        name = 'rcon_home',),
    url(
        regex = '^(?P<slug>[-\w]+)/rcon/status/$',
        view = rcon_views.refresh_status,
        name = 'rcon_refresh_status',),
    url(
        regex = '^(?P<slug>[-\w]+)/rcon/clients/$',
        view = rcon_views.refresh_clients,
        name = 'rcon_refresh_clients',),                
    url(
        regex = '^(?P<slug>[-\w]+)/rcon/execute/$',
        view = rcon_views.execute,
        name = 'rcon_command',),        
)

#
#urlpatterns = patterns('',
#    url(r'^$', views.home, name='game_admin'),
#    url(r'^execute/$', views.execute, name='admin_command'),
#    url(r'^ref/clients/$', views.refresh_clients, name='admin_refresh_clients'),
#    url(r'^ref/status/$', views.refresh_status, name='admin_refresh_status'),
#    url(r'^ban/list/$', views.banlist, name='admin_ban_list'),
#    url(r'^group/list/$', views.group_list, name='group_list_json'),
#)