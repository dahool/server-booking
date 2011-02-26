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
from django.forms import widgets
from django.utils.translation import ugettext_lazy as _
from models import Server

PASS_DEFAULT = '**********'

class ServerForm(forms.ModelForm):

    password = forms.RegexField(label=_("Password"),
                                widget=widgets.PasswordInput(attrs={'autocomplete':'off'}),
                                required=True,
                                max_length=50,
                                regex=r"^[-!\"#$%&'()*+,./:;<=>?@[\\\]_`{|}~a-zA-Z0-9]+$",
                                error_message = _("Non ascii chars are forbidden."),
                                initial=PASS_DEFAULT)
    
    class Meta:
        model = Server
        exclude = ("password", )

    def save(self, commit=True):
        server = super(ServerForm, self).save(commit=False)
        rp = self.cleaned_data['password']
        if rp != PASS_DEFAULT:
            server.rconpassword = rp
        if commit:
            server.save()
        return server