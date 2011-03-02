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

from django import forms
from django.utils.translation import ugettext_lazy as _

from djangoui.widgets import uiSplitDateTimeWidget

from models import Book
from djangoui.extras.widgets import SelectTimeWidget

class BookForm(forms.ModelForm):
    
    date_start = forms.SplitDateTimeField(('%d/%m/%Y',),('%H:%M',),
                                    widget=uiSplitDateTimeWidget(date_format="%d/%m/%Y",
                                                                 time_widget=SelectTimeWidget(show_seconds=False, minute_step=15)),
                                    label=_('Check-in'),
                                    required=True)
    date_end = forms.SplitDateTimeField(('%d/%m/%Y',),('%H:%M',),
                                    widget=uiSplitDateTimeWidget(date_format="%d/%m/%Y",
                                                                 time_widget=SelectTimeWidget(show_seconds=False, minute_step=15)),
                                    label=_('Check-out'),
                                    required=True)
            
    class Meta:
        model = Book
        #exclude = ("password", )