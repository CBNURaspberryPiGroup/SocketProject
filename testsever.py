import socket
import Commmand
import work
import Send


Host = ''
Port = 9966

storage = "./*"

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((Host,Port))
print("listening...")
server_socket.listen()
print("listened")
client_socket, addr = server_socket.accept()

print('Connected by '+str(addr))

wok=work()
wok.list_f()

print('고민성 ㅋ')
Com = Commmand()
Com.split()


client_socket.close()
server_socket.close()
