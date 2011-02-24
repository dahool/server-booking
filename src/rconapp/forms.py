from django import forms
from django.forms import widgets
from django.utils.translation import ugettext_lazy as _
from models import Server

class ServerForm(forms.ModelForm):

    password = forms.RegexField(label=_("Password"),
                                widget=widgets.PasswordInput(attrs={'autocomplete':'off'}),
                                required=False,
                                max_length=50,
                                regex=r"^[-!\"#$%&'()*+,./:;<=>?@[\\\]_`{|}~a-zA-Z0-9]+$",
                                error_message = _("Non ascii chars are forbidden."),
                                initial='')
    
    class Meta:
        model = Server
        exclude = ("password", )

    def save(self, commit=True):
        server = super(ServerForm, self).save(commit=False)
        rp = self.cleaned_data['password']
        if rp and rp <> '':
            server.set_password(rp)
        if commit:
            server.save()
        return server