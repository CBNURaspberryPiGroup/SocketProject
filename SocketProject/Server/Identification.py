from socket import socket
from cryptography.fernet import Fernet as fnet
from os.path import exists

class Identification:
    def __init__(self,client):
        self.client = client
        if not exists('Key.key'):
            self.key = fnet.generate_key()
            print(self.key)
            with open('Key.key','w') as f:
                f.write(str(self.key))
        else:
            with open('Key.key','r') as f:
                self.key = byte(f.readlines())
        if not exists('Auth.Data'):
            with open('Auth.Data','w'):
                pass
        
    def Authentification(self):
        client.sendall('ID'.encode())
        with open('Auth.Data','r'):
            
