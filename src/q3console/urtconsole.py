import re
from django.utils.translation import ugettext_lazy as _
from q3console.pyquake3 import PyQuake3

#    _commands['message'] = 'tell %s %s ^8[pm]^7 %s'
#    _commands['deadsay'] = 'tell %s %s [DEAD]^7 %s'
#    _commands['say'] = 'say %s %s'
#    _commands['set'] = 'set %s %s'
#    _commands['kick'] = 'clientkick %s %s'
#    _commands['ban'] = 'banid %s %s'
#    _commands['tempban'] = 'clientkick %s %s'
#    _commands['moveToTeam'] = 'forceteam %s %s'
    
class RconClient(object):

    color_re = re.compile(r'\^[0-9]')

    _gametype = {'ffa': 0,
                 'tdm': 3,
                 'ts': 4,
                 'ftl': 5,
                 'cah': 6,
                 'ctf': 7,
                 'bomb': 8}

    _gametype_detail = {'ffa': 'Free For All',
                 'tdm': 'Team Death Match',
                 'ts': 'Team Survivor',
                 'ftl': 'Follow The Leader',
                 'cah': 'Capture And Hold',
                 'ctf': 'Capture The Flag',
                 'bomb': 'Bomb'}
    
    def __init__(self, host, rconpassword):
        self.host = host
        self.rconpassword = rconpassword
        self.console = PyQuake3(host, rconpassword)
        self.console.update()

    def getservername(self):
        res = self._cvar("sv_hostname")
        return res
        
    def _clean_colors(self, text):
        if text:
            return self.color_re.sub('',text)
        return text
        
    def _normalize(self, data):
        if data:
            return data.encode('utf_8').strip()
        return data
    
    def _cvar(self, data):
        try:
            return self._clean_colors(self.console.vars(data))
        except:
            return None
        
    def _write(self, data):
        cmd, data = self.console.rcon(self._normalize(data))
        return data
    
    def map(self, data, action):
        if action=="get":
            data = self._cvar("mapname")
        else:
            data = self._write('map %s' % data)
        return data        
    
    def nextmap(self, data, action):
        if action=="get":
            data = self._cvar("g_nextmap")
        else:
            data = self._write('g_nextmap %s' % data)
        return data
        
    def cyclemap(self, data=None, action=None):
        data = self._write('cyclemap')
        return data

    def restartmap(self, data=None, action=None):
        data = self._write('restart')
        return data
    
    def reloadmap(self, data=None, action=None):
        data = self._write('reload')
        return data

    def bigtext(self, data, action=None):
        data = self._write('bigtext "^7%s"' % data)
        return data

    def say(self, data, action=None):
        data = self._write('say "^7%s"' % data)
        return data
        
    def _cvar_set(self, name, value):
        data = self._write('set %s %s' % (self._normalize(name), self._normalize(value)))
        return data
    
    def password(self, data, action):
        if action=="get":
            data = self._cvar('g_password')
        else:
            if data:
                data = self._cvar_set('g_password',data)
            else:
                data = self._cvar_set('g_password','')
        return data
                    
    def kick(self, data, action=None):
        data = self._write('clientkick %s' % data)
        return data   
    
    def gametype(self, data, action):
        # // TODO
        if action=="get":
            data = self._cvar('g_gametype')
            if data:
                i = int(data)
            if i == 0:
                t = 'ffa'
            elif i == 8:
                t = 'bomb'
            else:
                t = self.console.defineGameType(str(i))
            return self._gametype_detail[t]
        else:
            new_type = self._gametype[data]
            new_type_det = self._gametype_detail[data]
            self.console.write('g_gametype %d' % new_type)
            self.bigtext('^7Next game is ^3%s' % new_type_det)
            self.console.say('"^7Next game is ^3%s"' % new_type_det)
        return "Game type changed to: %s" % new_type_det

    def write(self, data, action=None):
        v = self.console.write(self._normalize(data))
        if v:
            return '%s => %s' % (data,getattr(v, 'getString', v))
        return data

    def cvar(self, data, action):
        if action=="get":
            v = self.console.getCvar("%s" % self._normalize(data))
            if v:
                return '%s => %s' % (data,v.getString())
            else:
                return 'Error (%s)' % data
        else:
            k,v = self._normalize(data).split(' ')
            self.console.setCvar(k,v)
            return '%s => %s' % (k,v)
        
