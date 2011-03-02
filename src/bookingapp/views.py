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
from django.contrib.auth.decorators import login_required
from django.views.generic.list_detail import object_detail, object_list
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

from common.view.decorators import render
from bookingapp.models import Book
from bookingapp.forms import BookForm

from rconapp.models import Server

@login_required
@render('bookingapp/book_form.html')
def book_create_update(request, pk=None):
    res = {}
    if request.method == 'POST':
        if pk:
            b = get_object_or_404(Book, pk=pk)
            res['book']=b
            form = BookForm(request.POST, instance=b)
        else:
            form = BookForm(request.POST)
        if form.is_valid():
            b = form.save(False)
            b.user = request.user
            b.save()
            return HttpResponseRedirect(b.get_absolute_url())
        res['form'] = form
    else:
        if pk:
            b = get_object_or_404(Book, pk=pk)
            res['book']=b
            form = BookForm(instance=b)
        else:
            if request.GET.has_key('s'):
                s = get_object_or_404(Server, slug=request.GET['s'])
                form = BookForm(initial={'user': request.user, 'server': s})
            else:
                form = BookForm(initial={'user': request.user})
        res['form'] = form 
    return res

@login_required
def book_list(request):
    return object_list(request,
                       queryset=Book.objects.all_active().filter(user=request.user),
                       template_object_name='book')
    
@login_required
def book_detail(request, pk):
    return object_detail(request,
                         queryset=Book.objects.all(),
                         template_object_name='book',
                         object_id=pk)