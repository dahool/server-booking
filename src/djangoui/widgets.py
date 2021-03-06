from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.translation import get_language
from djangoui.extras.widgets import SelectTimeWidget

UI_VERSION = getattr(settings, 'UI_VERSION', '1.8.4') 
UI_PATH = getattr(settings, 'UI_PATH', 'ui/')
UI_THEME = getattr(settings, 'UI_THEME', 'dot-luv')
JQUERY_UI_JS = 'jquery-ui-' + UI_VERSION + '.custom.min.js'
JQUERY_UI_CSS = 'jquery-ui-' + UI_VERSION + '.custom.css'

class uiTimeInput(forms.widgets.TimeInput):
    format = '%H:%M' 
    
    class Media:
        css = {
            'screen': (settings.MEDIA_URL + UI_PATH + UI_THEME + '/' + JQUERY_UI_CSS,
                       settings.MEDIA_URL + UI_PATH + 'jquery.timemachine.css',)
        }
        js = (settings.MEDIA_URL + UI_PATH + JQUERY_UI_JS,
              settings.MEDIA_URL + UI_PATH + 'jquery.timemachine-1.0.0.min.js',)

    def __init__(self, attrs={}):
        super(uiTimeInput, self).__init__(attrs={'class': 'time-select-widget', 'size': '5', 'autocomplete': 'off'}, format=self.format)
        
    def render(self, name, value, attrs=None):
        elementId = attrs.get('id')
        html = super(uiTimeInput, self).render(name, value, attrs)
        html += u"<script type=\"text/javascript\">$(function(){$('#%s').timemachine({format:\"24\"});});</script>" % elementId
        return mark_safe(html)
            
class uiDateInput(forms.widgets.DateInput):
    class Media:
        css = {
            'screen': (settings.MEDIA_URL + UI_PATH + UI_THEME + '/' + JQUERY_UI_CSS,
                       settings.MEDIA_URL + UI_PATH + 'style.css',)
        }
        js = (settings.MEDIA_URL + UI_PATH + JQUERY_UI_JS,)

    def __init__(self, attrs=None, format=None):
        self.language = get_language()[:2]
        if attrs is None: attrs = {}
        defaultattrs = {'class': 'date-select-widget', 'size': '12', 'autocomplete': 'off'} 
        defaultattrs.update(attrs)
        super(uiDateInput, self).__init__(attrs=defaultattrs, format=format)
        
    def render(self, name, value, attrs=None):
        html = super(uiDateInput, self).render(name, value, attrs)
        if self.language != "en":
            html += u'<script type="text/javascript" src="%sui/jquery/jquery.ui.datepicker-%s.js"></script>' % (settings.MEDIA_URL, self.language)        
        html += u"<script type=\"text/javascript\">$(function(){$('.date-select-widget').datepicker({showAnim: '', dateFormat: '%s'});});</script>" % python_to_js_dateformat(self.format)
        return mark_safe(html)
    
class uiSplitDateTimeWidget(forms.widgets.MultiWidget):
    """
    A Widget that splits datetime input into two <input type="text"> boxes.
    The original SplitDateTimeWidget doesn't let me change the inner widgets
    """
    date_format = uiDateInput.format

    def __init__(self, attrs=None, date_format=None, time_widget = None, show_seconds = None):
        if date_format:
            self.date_format = date_format
        if not time_widget:
            time_widget = SelectTimeWidget(attrs=attrs, show_seconds=show_seconds)
        widgets = (uiDateInput(attrs=attrs, format=self.date_format),
                   time_widget)
        super(uiSplitDateTimeWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.date(), value.time().replace(microsecond=0)]
        return [None, None]

def python_to_js_dateformat(format):
    return format.replace("%b", "M").replace("%B", "MM").replace("%d", "dd").replace("%m", "mm").replace("%Y", "yy").replace("%y", "y")
    
    