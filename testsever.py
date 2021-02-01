import socket
import Commmand
import work
import Send

wrk = work.filelist()
Com = Commmand.Command()
sed = Send.SendData()

Host = ''
Port = 9966

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((Host,Port))
print("listening...")
server_socket.listen()
print("listened")
client, addr = server_socket.accept()

print('Connected by '+str(addr))



wrk()
print('고민성 ㅋ')
Com.split()

client.close()
server_socket.close()
