import time

from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.db.models import Q
from django.utils.translation import gettext as _
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from django.core import validators
from django.utils.encoding import smart_unicode
from django.conf import settings

from common.view.decorators import render
from common.shortcuts import get_object_or_404
from common.decorators import superuser_required
from common.middleware.exceptions import Http403

from rconapp.models import Server
from q3console.urtconsole import UrtClient

class Status(object):
    pass

@render('rconapp/rcon/home.html')
def home(request, slug):
    server = get_object_or_404(Server, slug=slug)
    console = UrtClient(server.host, server.rconpassword)
    status = Status()
    status.gametype =console.get_gametype()
    status.map = console.get_map()
    return {'server': server,
            'status': status}
    
@superuser_required
@render('webfront/admin/status.html')
def refresh_status(request):
    status = None
    return {'status': status}
                
@superuser_required    
def execute(request):
    if request.method != 'POST':
        raise Http403
    server = request.session.get('server')
    cfgfile = settings.SERVERS[server]['CFG']
    try:
        c = None
    except Exception, e:
        res = str(e)
    else:
        # get server name to check if we have connection
        if c.getservername() is None:
            res = _('<span style=\'color: #F00\'>Can\'t establish RCON link</span>')
        else:
            command = request.POST.get('cmd')
            action = request.POST.get('action')
            data = request.POST.get('data')
            try:
                method = getattr(c, command)
            except:
                res = _("Unknown command %s" % command)
            else:
                try:
                    res = method(data, action)
                except Exception, e:
                    res = str(e)
    return HttpResponse(res)