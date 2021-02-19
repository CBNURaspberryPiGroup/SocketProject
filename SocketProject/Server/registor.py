 
from socket import socket
from cryptography.fernet import Fernet as fnet
from os.path import exists

class Identification:
    def __init__(self,client):
        self.client = client
        if not exists('Key.key'):
            self.__key = fnet.generate_key()
            print(self.__key)
            with open('Key.key','w') as f:
                f.write(str(self.__key)[2:-1])
        else:
            with open('Key.key','r') as f:
                self.__key = f.read().encode()
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
                    id = f.readline().encode()[:-1]
                    psswd = f.readline().encode()[:-1]
                    if id == b'' : break
                    self.__Base[id] = psswd
            except Exception:
                pass
        print("Database Opened")
        print(self.__Base)
                
    def DatabaseWrite(self):
        with open('Auth.Data','w') as f:
            for id in self.__Base.keys():
                f.write(id.decode()+'\n')
                f.write(self.__Base[id].decode()+'\n')
        print("Database Saved")
        
    def Authentification(self):
        while True : 
            self.client.sendall('ID:'.encode())
            id = self.client.recv(1024)
            if not( id in self.__Base):
                self.client.sendall('ID Not Found'.encode())
            else : break
        while True :
            self.client.sendall('Password:'.encode())
            passwd = self.client.recv(1024)
            if passwd != self.__crypt.decrypt(self.__Base[id]):
                self.client.sendall('Wrong Password'.encode())
            else : 
                print("Authentification Finished")
                break
            
                
            
    def Register(self):
        while True :
            self.client.sendall('Register: ID:'.encode())
            id = self.client.recv(1024)
            if id in self.__Base :
                self.client.sendall('ID Already Exists'.encode())
            else : 
                self.client.sendall('ID is available'.encode())
                break
            
        
        while True :
            self.client.sendall('Password:'.encode())
            passwd = self.client.recv(1024)
            self.client.sendall('Password Confirm:'.encode())
            if self.client.recv(1024) != passwd:
                self.client.sendall('Password Confirm Failed'.encode())
            else : self.client.sendall('Sign up complete'.encode())       
            self.__Base[id] = self.__crypt.encrypt(passwd)
            self.DatabaseWrite()
            print("Register Finished")
            break
            
                    
       
        