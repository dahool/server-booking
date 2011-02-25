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
        regex = '^(?P<slug>[-\w]+)/rcon/execute/$',
        view = rcon_views.home,
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