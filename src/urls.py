# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

#================================================================
from django.core import urlresolvers
from django.http import HttpResponse

def show_url_patterns(request):
    patterns = _get_named_patterns()
    r = HttpResponse("", content_type = 'text/html')
    longest = max([len(pair[0]) for pair in patterns])
    for key, value in patterns:
        if value.rfind("%") == -1:
            r.write('<a href="%s">%s</a><br/>' % (value, key.ljust(longest + 1)))
    return r

def _get_named_patterns():
    "Returns list of (pattern-name, pattern) tuples"
    resolver = urlresolvers.get_resolver(None)
    patterns = sorted([
        (key, value[0][0][0])
        for key, value in resolver.reverse_dict.items()
        if isinstance(key, basestring)
    ])
    return patterns
#================================================================

urlpatterns = patterns('',
    url(r'^$', show_url_patterns, name='home'),
    url('^server/', include('rconapp.urls')),
    url('^admin/', include(admin.site.urls)),
)
       
if settings.STATIC_SERVE:
    urlpatterns += patterns('',
        (r'^sitemedia/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )