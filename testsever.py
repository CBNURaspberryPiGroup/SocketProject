import socket
import Command.py
import work.py
import Send.py

Host = '172.30.1.35'
Port = 9966

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((Host,Port))
print("listening...")
server_socket.listen()
print("listened")
client_socket, addr = server_socket.accept()

print('Connected by '+str(addr))

filelist.fileinf()
Command()

client_socket.close()
server_socket.close()
