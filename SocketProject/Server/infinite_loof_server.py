import socket
import Commmand
import work
import Send


Host = ''
Port = 9966

storage = "./"

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

a = 0

while 1 :
    a += 1
    server_socket.bind((Host,Port))
    print("listening...")
    server_socket.listen()
    print("listened")
    client, addr = server_socket.accept()
    print('Connected by '+str(addr))
    Com = Commmand.Command(client,storage)
    if a == 1 : 
        Com.split2()
    wok=work.filelist(client,storage)
    wok.list_f()
    Com.split()