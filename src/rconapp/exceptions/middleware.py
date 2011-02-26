from django.http import HttpResponseServerError
from django.template import loader, Context
from django.contrib import messages

from rconapp.exceptions import ApplicationError

def applicationErrorResponse(request, message, template_name='error.html'):
    messages.error(request, message)
    t = loader.get_template(template_name)
    c = Context({
        'request': request,
    })
    return HttpResponseServerError(t.render(c))

class AppExceptionHandler(object):
         
    def process_exception(self, request, exception):
        if isinstance(exception, ApplicationError):
            return applicationErrorResponse(request, exception.message)
        else:
            return None