# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'TODO', name='home'),
    url('^admin/', include(admin.site.urls)),
)
       
if settings.STATIC_SERVE:
    urlpatterns += patterns('',
        (r'^webmedia/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )