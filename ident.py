import socket

def listen(addr, port, user):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((addr, port))
    server.settimeout(600)
    server.listen(1)
    con, other = server.accept()
    query = con.recv(64)
    query = query.decode()
    con.sendall((query + " : USERID : IRC : " + user).encode())

listen("", 113, "pyre")