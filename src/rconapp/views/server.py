import time

from django.conf import settings
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.db.models import Q
from django.utils.translation import gettext as _
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.cache import cache_page
from django.core import validators
from django.utils.encoding import smart_unicode

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic.list_detail import object_detail, object_list

from common.view.decorators import render
from common.shortcuts import get_object_or_404
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
            if not s.is_maintainer(request.user):
                raise Http403
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
    s = get_object_or_404(Server, slug=slug)
    return object_detail(request,
                         queryset=Server.objects.all(),
                         template_object_name= 'server',
                         slug=slug)
        
#@login_required
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