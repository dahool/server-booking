import re
from q3console.pyiourt import PyIoUrt as Console
    
class UrtClient(object):

    color_re = re.compile(r'\^[0-9]')

    _gametype = {'0': 'ffa',
                 '3': 'tdm',
                 '4': 'ts',
                 '5': 'ftl',
                 '6': 'cah',
                 '7': 'ctf',
                 '8': 'bomb'}
    
    _gametype_rev = {'ffa': '0',
                 'tdm': '3',
                 'ts': '4',
                 'ftl': '5',
                 'cah': '6',
                 'ctf': '7',
                 'bomb': '8'}
    
    def __init__(self, host, rconpassword):
        self.host = host
        self.rconpassword = rconpassword
        self.console = Console(host, rconpassword)
        self.console.update()

    def getservername(self):
        return self.get_cvar("sv_hostname")
        
    def player_list(self):
        self.console.rcon_update()
        return self.console.players
    
    def _clean_colors(self, text):
        if text:
            return self.color_re.sub('',text)
        return text
        
    def _normalize(self, data):
        if data:
            return data.encode('utf_8').strip()
        return data
    
    def get_cvar(self, data):
        try:
            return self._clean_colors(self.console.vars[self._normalize(data)])
        except IndexError:
            return None

    def set_cvar(self, name, value):
        data = self._write('set %s %s' % (self._normalize(name), self._normalize(value)))
        return data
    
    def write(self, data):
        cmd, data = self.console.rcon(self._normalize(data))
        return data
    
    def cyclemap(self):
        data = self.write('cyclemap')
        return data

    def restartmap(self):
        data = self.write('restart')
        return data
    
    def reloadmap(self):
        data = self.write('reload')
        return data

    def bigtext(self, data):
        data = self.write('bigtext "^7%s"' % data)
        return data

    def say(self, data):
        data = self.write('say "^7%s"' % data)
        return data
                    
    def kick(self, data):
        data = self.write('clientkick %s' % data)
        return data   

    def slap(self, data):
        data = self.write('slap %s' % data)
        return data
        
    def set_map(self, data):
        self.write('map %s' % data)
        
    def get_map(self):
        return self.get_cvar('mapname')

    def set_nextmap(self, data):
        self.set_cvar('g_nextmap', data)
        
    def get_nextmap(self):
        return self.get_cvar('g_nextmap')
    
    def set_password(self, data):
        self.set_cvar('g_password', data)
        
    def get_password(self):
        return self.get_cvar('g_password')
        
    def set_gametype(self, data):
        self.set_cvar('g_gametype', self._gametype_rev[data])
        
    def get_gametype(self):
        return self._gametype[self.get_cvar('g_gametype')]
        
