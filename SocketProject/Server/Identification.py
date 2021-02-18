from socket import socket
from cryptography.fernet import Fernet as fnet
from os.path import exists
import base64

class Identification:
    def __init__(self,client):
        self.client = client
        if not exists('Key.key'):
            self.__key = fnet.generate_key()
            print(self.__key)
            with open('Key.key','w') as f:
                f.write(str(self.__key))
        else:
            with open('Key.key','r') as f:
                self.__key = base64.b64encode(f.read().encode())
        self.__crypt = fnet(self.__key)
        self.DatabaseOpen()
    
    def DatabaseOpen(self):
        if not exists('Auth.Data'):
            with open('Auth.Data','w'):
                pass
        with open('Auth.Data','r') as f:
            self.__Base = {}
            try:
                while(True):
                    self.__Base[f.readlines()] = f.readlines()
            except Exception:
                pass
        print("Database Opened")
                
    def DatabaseWrite(self):
        if exists('Auth.Data'):
            with open('Auth.Data','w') as f:
                for id in self.__Base.keys():
                    f.write(id)
                    f.write(self.__Base[id])
        print("Database Saved")
        
    def Authentification(self):
        self.client.sendall('ID:'.encode())
        id = self.client.recv()
        if not id in self.__Base:
            self.client.sendall('ID Not Found'.encode())
            return False
        self.client.sendall('Password:'.encode())
        passwd = self.client.recv()
        if password != self.__crypt.decrypt(self.__Base[id]):
            self.client.sendall('Wrong Password'.encode())
            return False
        return True
            
    def Register(self):
        self.client.sendall('Register: ID:'.encode())
        id = self.client.recv()
        if id in self.__Base :
            self.client.sendall('ID Already Exists'.encode())
            return False
        self.client.sendall('Password:'.encode())
        passwd = self.client.recv()
        self.client.sendall('Password Confirm:')
        if self.client.recv() != passwd:
            self.client.sendall('Password Confirm Failed'.encode())
            return False
        self.__Base[id] = self.__crypt.encrypt(passwd)
        self.DatabaseWrite()
        return True
