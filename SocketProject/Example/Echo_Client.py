import socket

Host = "203.227.140.199"
#Host = "192.168.0.15"
Port = 9966

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client_socket.connect((Host,Port))

client_socket.sendall('Hello'.encode())

data = client_socket.recv(1024)
print('Received',repr(data.decode()))

client_socket.close()
