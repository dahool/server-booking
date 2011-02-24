from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    url(
        regex = '^add/$',
        view = server_create_update,
        name = 'server_create'),
    url(
        regex = '^(?P<slug>[-\w]+)/edit/$',
        view = server_create_update,
        name = 'server_edit',),
    url(
        regex = '^(?P<slug>[-\w]+)/delete/$',
        view = server_delete,
        name = 'server_delete',),
) 

urlpatterns += patterns('django.views.generic',
    url(
        regex = '^(?P<slug>[-\w]+)/$',
        view = server_detail,
        name = 'server_detail'),
    url (
        regex = '^$',
        view = server_list,
        name = 'server_list'),
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