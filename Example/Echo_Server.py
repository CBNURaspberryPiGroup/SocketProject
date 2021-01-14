import socket

Host = ""
Port = 9966

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((Host,Port))
print("listening...")
server_socket.listen()
print("listened")
client_socket, addr = server_socket.accept()

print('Connected by '+str(addr))

while True:
    data = client_socket.recv(1024)
    if not data: break
    print('Received from %s %s'%(addr,data.decode()))
    client_socket.sendall(data)

client_socket.close()
server_socket.close()
