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
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink

from common.fields import AutoSlugField
from common.crypto import BCipher

class Server(models.Model):
    slug = AutoSlugField(max_length=50, unique=True, editable=False,
                            prepopulate_from="name", force_update=False)    
    name = models.CharField(max_length=50, unique=True, verbose_name=_('Name')) 
    ip = models.IPAddressField(verbose_name=_('IP Address'))
    port = models.IntegerField(verbose_name=_('Port'), default=27960)
    password = models.CharField(max_length=50)
    admin = models.EmailField(verbose_name=_('Contact e-mail'))
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=True, editable=False)
    
    def __unicode__(self):
        return u'%s [%s:%d]' % (self.name, self.ip, self.port)

    def __repr__(self):
        return '<Server: %s>' % self.name
        
    def _set_password(self, clear_text):
        bc = BCipher()
        setattr(self, 'password', bc.encrypt(clear_text))
    
    def _get_password(self):
        value = getattr(self, 'password')
        if value is not None:
            bc = BCipher()
            return bc.decrypt(value)
        return value
    
    rconpassword = property(_get_password, _set_password)
    
    class Meta:
        ordering  = ('name',)
        get_latest_by = 'created'    
        permissions = (
            ("change_map", _("Can change map")),
            ("change_nextmap", _("Can change next map")),
            ("change_password", _("Can change password")),
            ("change_gametype", _("Can change gametype")),
            ("send_say", _("Can send console message")),
            ("send_bigtext", _("Can execute bigtext")),
            ("reload_map", _("Can reloap map")),
            ("write_console", _("Can write to console")),
            ("change_cvar", _("Can change cvars")),
            ("view_online", _("Can view online clients")),
            ("kick_client", _("Can kick client")),
            ("slap_client", _("Can slap client")),
        )
    
    @property
    def host(self):
        return "%s:%s" % (self.ip, self.port)
    
    @permalink
    def get_absolute_url(self):
        return ('server_detail', None, { 'slug': self.slug })    