import socket
import ssl
from threading import Thread
from time import sleep

def main():
  print("Pyrecd initializing...")
  server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server.bind(("localhost", 6667))
  server.listen(1)
  sock, other= server.accept()
  print(sock)
  sock.sendall(b"Hello world!\n")
  sleep(5)
  
main()