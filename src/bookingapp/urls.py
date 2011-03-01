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

from django.conf.urls.defaults import *
from bookingapp import views

urlpatterns = patterns('',
    url(
        regex = '^create/$',
        view = views.book_create_update,
        name = 'book_create'),
    url(
        regex = '^(?P<pk>[-\w]+)/edit/$',
        view = views.book_create_update,
        name = 'book_edit',),
) 

urlpatterns += patterns('django.views.generic',
    url(
        regex = '^(?P<pk>[-\w]+)/details/$',
        view = views.book_detail,
        name = 'book_detail'),
    url(
        regex = '^$',
        view = views.book_list,
        name = 'book_list'),        
)