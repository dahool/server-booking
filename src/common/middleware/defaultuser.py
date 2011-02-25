from django.conf import settings

class DefaultLoggedUser(object):
    
    def process_request(self, request):
        if not hasattr(request, 'user'):
            from django.contrib.auth import authenticate, login
            user = authenticate(username=getattr(settings, 'DEFAULT_USER', 'admin'), password=getattr(settings, 'DEFAULT_USER_PASS', 'admin'))
            if user:
                login(request, user)
        return None