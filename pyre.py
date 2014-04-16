from configparser import SafeConfigParser

class Pyre:
    def __init__(self, opts):
        self.server = opts['server']
        self.port = opts['port']
        self.ssl = opts['ssl']
        self.password = opts['password']
        self.nick = opts['nick']
        self.ident = opts['ident']
        self.realname = opts['realname']
        self.usermode = opts['usermode']
        self.version = opts['version']
        self.finger = opts['finger']
        self.userinfo = opts['userinfo']

    def connect(self):
        pass

    def connect(self, server):
        self.server = server
        self.connect()

    def connect(self, server, port):        
        self.port = port
        self.connect(server)

    def connect(self, server, port, ssl):        
        self.ssl = ssl
        self.connect(server, port)

    def conect(self, server, port, ssl, password):
        self.password = password
        self.connect(server, port, ssl)
    
def main():
    parser = SafeConfigParser()
    parser.read('config.ini')

    options = {}
    options['server'] = parser.get('network','server')
    options['port'] = parger.get('network','port')
    options['ssl'] = (port[0] == '+')
    options['port'] = int(port)
    options['password'] = parser.get('network', 'password')

    options['nick'] = parser.get('bot', 'nick')
    options['ident'] = parser.get('bot', 'ident')
    options['realname'] = parser.get('bot', 'realname')
    options['usermode'] = parser.get('bot', 'usermode')

    options['version'] = parser.get('ctcp', 'version')
    options['finger'] = parser.get('ctcp', 'finger')
    options['userinfo'] = parser.get('ctcp', 'userinfo')    
    
    bot = new Pyre(options)
main()
