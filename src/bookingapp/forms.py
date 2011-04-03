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
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from djangoui.widgets import uiSplitDateTimeWidget

from models import Book
from djangoui.extras.widgets import SelectTimeWidget

import datetime
from common.utils.functions import timeDeltaToSeconds, duration_human

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
    
    def clean_date_start(self):
        dt = self.cleaned_data['date_start']
        now = datetime.datetime.now()
        if dt <= now:
            raise forms.ValidationError("You can't book a date in the past")
        if (dt - now) > settings.MAX_BOOKING_ADVANCE:
            sec = timeDeltaToSeconds(settings.MAX_BOOKING_ADVANCE)
            raise forms.ValidationError("You can't book more than %s in advance" % duration_human(sec))
        return dt
    
    def clean_date_end(self):
        dt = self.cleaned_data['date_start']
        de = self.cleaned_data['date_end']
        print dt
        print de
        if de < dt:
            raise forms.ValidationError("Are you serious? End time should be after start time")
        if (de - dt) < settings.MIN_BOOKING_TIME:
            sec = timeDeltaToSeconds(settings.MIN_BOOKING_TIME)
            raise forms.ValidationError("Minimun booking time is %s" % duration_human(sec))
        return de
     
    class Meta:
        model = Book
        #exclude = ("password", )