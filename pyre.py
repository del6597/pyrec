from configparser import SafeConfigParser
import datetime
import multiprocessing
import socket
import ssl
import queue
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
        self.sendq = queue.Queue()# PriorityQueue() -- Maybe later
        self.error = False
        self.binds = {}
        self.bind("001", self.welcome)

    def read(self):
        rec = self.sock.recv(512)
        buff =''
        while(rec.decode() != '' and not self.error):
            buff = buff + rec.decode()
            if '\n' in buff:
                coms = str.split(buff, '\n')
                for i in range(len(coms)-1):
                    print("["+str(datetime.datetime.now().time())+"] "+coms[i])
                    if coms[i].startswith("PING"): #Skip the queue for PINGS
                        self.sock.sendall(("PONG" + coms[i][4:] + "\n").encode())
                    elif coms[i].startswith("ERROR"):
                        self.error = True
                    else:
                        split = str.split(coms[i])
                        #need something here to say 'run through all these plugins and broadcast them events
                        binds = self.binds.setdefault(split[1], [])
                        for b in binds:
                            b(self, coms[i])
                buff = coms[-1]
            rec = self.sock.recv(512)
        self.connected = False

    def bind(self, bind, handler):
        b = self.binds.setdefault(bind, [])
        b.append(handler)
        self.binds[bind] = b
        
    def write(self, text, immed=False):
        if(not text.endswith("\n")):
            #self.sock.sendall((text + "\n").encode())
            self.sendq.put((text + "\n"))
        else:
            #self.sock.sendall(text.encode())
            self.sendq.put(text)

    def send(self):
        while(self.connected and not self.error):
            text = self.sendq.get()
            self.sock.sendall(text.encode())
            print("["+str(datetime.datetime.now().time())+"] "+ text)
            sleep(1.5) # Adjust as needed
        
    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if(self.ssl):
            self.sock = ssl.wrap_socket(self.sock)
        self.sock.settimeout(300)
        self.sock.connect((self.server, self.port))
        
        # Starts our read io thread
        readthread = Thread(target=self.read)
        readthread.start()
        
        register = ""
        if(self.password!=None):
            register = "PASS " + self.password +'\n'
        register += "NICK " + self.nick +'\n'
        register += "USER " + self.ident + " 8 * :" + self.realname + '\n'
        self.sock.sendall(register.encode())        

    def cmd(self, cmd, params, rest=""):
        cmd = str.upper(str(cmd)) + " "
        p = ""
        for i in params:
            p += str(i) + " "        
        self.write(cmd + p + rest)
        
    def notice(self, target, msg):
        self.cmd("NOTICE", [target], ":" + msg)
        
    def msg(self, target, msg):
        self.cmd("PRIVMSG", [target], ":" + msg)
    
    def invite(self, target, channel):
        self.cmd("INVITE", [target, channel])
        
    def join(self, target, key=None):
        self.cmd("JOIN", [target, key])
        
    def welcome(self, bot, line):
        self.connected = True
        # Start our sendq thread
        writethread = Thread(target=self.send)
        writethread.start()
        
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
    
    # Dumb CLI
    text = input()
    while(not text.startswith("QUIT") and not bot.error and bot.connected):
        bot.write(text)
        text = input()
    bot.write(text)
    
main()
