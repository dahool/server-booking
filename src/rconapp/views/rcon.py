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

from q3console.console.client import B3Client
from q3console.console.serverinfo import ServerInfo

from rconapp.models import Server

@render('rconapp/rcon/home.html')
def home(request, slug):
    server = get_object_or_404(Server, slug=slug)
    #clients = _client_list(request)
    #status = _status(request)
    return {'server': server}

def _status(request):
    status = {}
    server = request.session.get('server')
    cfgfile = settings.SERVERS[server]['CFG']
    try:
        c = B3Client(cfgfile)
    except:
        pass
    else:
        status['map'] = c.console.getMap()
        status['type'] = c.gametype(data=None, action='get')
    return status
    
@superuser_required
@render('webfront/admin/status.html')
def refresh_status(request):
    status = _status(request)
    return {'status': status}
    
@superuser_required
@render('webfront/admin/clients.html')
def refresh_clients(request):
    clients = _client_list(request, False)
    return {'clients': clients}
                
def _client_list(request, m=True):
    s = None
    try:
        s = ServerInfo(request.session.get('server'))
    except:
        # try again
        time.sleep(1)
    try:
        if not s:
            s = ServerInfo(request.session.get('server'))
        clients = s.getPlayerList()
    except Exception, e:
        if m:
            messages.error(request, _('Error: %s') % str(e))
        clients=[]
    return clients
    
@superuser_required    
def execute(request):
    if request.method != 'POST':
        raise Http403
    server = request.session.get('server')
    cfgfile = settings.SERVERS[server]['CFG']
    try:
        c = B3Client(cfgfile)
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