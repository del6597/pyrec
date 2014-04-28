from configparser import SafeConfigParser
import datetime
import socket
import ssl
from threading import Thread
from time import sleep

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

    def read(self):
        rec = self.sock.recv(512)
        buff =''
        while(rec.decode() != ''):
            buff = buff + rec.decode()
            if '\n' in buff:
                coms = str.split(buff, '\n')
                for i in range(len(coms)-1):
                    print("["+str(datetime.datetime.now().time())+"] "+coms[i])
                    if coms[i].startswith("PING"):
                      self.sock.sendall(("PONG" + coms[i][4:] + "\n").encode())
                    else:
                      pass
                buff = coms[-1]
            rec = self.sock.recv(512)        

    def write(self, text):
        if(not text.endswith("\n")):
            self.sock.sendall((text + "\n").encode())
        else:
            self.sock.sendall(text.encode())
        print("["+str(datetime.datetime.now().time())+"] "+text)

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if(self.ssl):
            self.sock = ssl.wrap_socket(self.sock)
        self.sock.settimeout(300)
        self.sock.connect((self.server, self.port))
        thread = Thread(target=self.read)
        thread.start()
        if(self.password!=None):
            self.write("PASS " + self.password)
        self.write("NICK " + self.nick)
        self.write("USER " + self.ident + " 8 * :" + self.realname)
        # sleep(5) # Not a good solution
        # self.write("NS identify password") # ID to nickserv
        text = input()
        while(not text.startswith("QUIT")):
          self.write(text)
          text = input()
        self.write(text)
        #self.sock.close()
    
def main():
    defaults = {'network': {'server': None, 'port': 6667, 'password': None}, \
                'bot': {'nick': 'Pyre', 'ident': 'pyro', 'realname': 'Pyre', 'usermode': '+iwx'}, \
                'ctcp': {'version': 'Pyre IRC', 'finger': 'Pyre IRC', 'userinfo': 'Pyre IRC'}}
    parser = SafeConfigParser(defaults)
    parser.read('config.ini')

    options = {}
    options['server'] = parser.get('network','server')
    options['port'] = parser.get('network','port')
    options['ssl'] = (options['port'][0] == '+')
    options['port'] = int(options['port'])
    options['password'] = parser.get('network', 'password')

    options['nick'] = parser.get('bot', 'nick')
    options['ident'] = parser.get('bot', 'ident')
    options['realname'] = parser.get('bot', 'realname')
    options['usermode'] = parser.get('bot', 'usermode')

    options['version'] = parser.get('ctcp', 'version')
    options['finger'] = parser.get('ctcp', 'finger')
    options['userinfo'] = parser.get('ctcp', 'userinfo')    
    
    bot = Pyre(options)
    bot.connect()
main()
