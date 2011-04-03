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
from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink
from django.contrib.auth.models import User
from django.db.models import Q

from rconapp.models import Server

class BookManager(models.Manager):
    
    def all_active(self):
        return self.filter(Q(cancelled=False) | Q(date_end__gte=datetime.now()))

class Book(models.Model):
    server = models.ForeignKey(Server, related_name="bookings", verbose_name=_('Server'))
    user = models.ForeignKey(User, editable=False)
    date_start = models.DateTimeField(verbose_name=_('Check-in'))
    date_end = models.DateTimeField(verbose_name=_('Check-out'))
    password = models.CharField(max_length=10, verbose_name=_('Choose a password'))
    cancelled = models.BooleanField(default=False, editable=False) 
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=True, editable=False)
    
    objects = BookManager()
    
    def __unicode__(self):
        return u'%s - %s' % (self.server.name, self.date_start)

    def __repr__(self):
        return '<Book: %s>' % self.server.name
        
    class Meta:
        get_latest_by = 'created'
        ordering = ['date_start']
            
    @permalink
    def get_absolute_url(self):
        return ('book_detail', None, { 'pk': self.pk })