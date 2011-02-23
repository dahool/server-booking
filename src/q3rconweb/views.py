import time

from django.conf import settings
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

from common.view.decorators import render
from common.shortcuts import get_object_or_404
from common.decorators import superuser_required
from common.middleware.exceptions import Http403

from b3connect.console.client import B3Client
from b3connect.console.serverinfo import ServerInfo

@superuser_required
@render('webfront/admin/home.html')
def home(request):
    clients = _client_list(request)
    status = _status(request)
    return {'clients': clients,
            'status': status,
            'maps': Map.objects.all()}

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
        if is_plugin_installed('status'):
            from plugins.status import get_server_status
            status = get_server_status(request.session.get('server'))
            if status.clients:
                if m:
                    messages.info(request, _('Using alternative players info method'))
                for c in status.clients:
                    try:
                        ci = Client.objects.using(request.session.get('server')).get(id=c.id)
                    except Client.DoesNotExist:
                        pass
                    else:
                        setattr(ci, 'cid', c.cid)
                        clients.append(ci)
                if status.totalClients!=len(clients):
                    if m:
                        messages.warning(request, _('The information is not accurate'))
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

@cache_page(180*60)
@render('json')
def group_list(request):
    dict = {}
    for group in Group.objects.using(request.session.get('server')).all():
        dict[group.id]=str(group)
    return dict 

@superuser_required
@render('webfront/admin/banlist.html')
def banlist(request):
    if request.method == 'POST':
        if request.POST.has_key('addip') and request.POST.get('addip'):
            value = request.POST.get('addip').strip()
            if not validators.ipv4_re.search(smart_unicode(value)):
                messages.error(request, _(u'Enter a valid IPv4 address.'))
            else:
                try:
                    c = B3Client(settings.SERVERS[request.session.get('server')]['CFG'])
                except Exception, e:
                    messages.error(request, str(e))
                else:
                    c.write("addIP %s" % smart_unicode(value))
        if request.POST.has_key('ip'):
            try:
                c = B3Client(settings.SERVERS[request.session.get('server')]['CFG'])
            except Exception, e:
                messages.error(request, str(e))
            else:
                for ip in request.POST.getlist('ip'):
                    c.write("removeIP %s" % smart_unicode(ip))
                    
    list = load_banlist(settings.SERVERS[request.session.get('server')]['BANLIST'])
    return {'list': list}