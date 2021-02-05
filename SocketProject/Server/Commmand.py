from socket import *
import os
from os.path import exists
import sys
import Send





class Command():
    
    def __init__(self,client,storage):
        
        self.storage = storage
        self.client = client
       
        
        
    def split(self):
        filename = self.client.recv(1024)
        filename = filename.decode()
        self.split_f = filename.split(' ')  
        
        if self.split_f[0] == 'push':
            if not exists(self.split_f[1]):
                err = ('Error -'+self.split_f[1]+'- 존재하지 않는 파일 입니다') 
                self.client.sendall(err.encode('utf-8'))
                
                print(err)
            else:    
                self.file_push()
            
        elif self.split_f[0] == 'pull':
            if not exists(self.split_f[1]):
                err = ('Error -'+self.split_f[1]+'- 존재하지 않는 파일 입니다') 
                self.clinet.sendall(err.encode('utf-8'))
                
                print(err)
            else:    
                self.file_pull()
        
        else:
            err = ('Error -'+self.split_f[0]+'- 존재하지 않는 명령어 입니다')
            print(err) 
            self.clinet.sendall(err.encode('utf-8'))
                  
    def file_push(self):
        fileExtension = os.path.splitext(self.split_f[1])[1]
        print(fileExtension)
        
        
        
        
        
            
            
            

              
    def file_pull(self):
        filename, fileExtension = os.path.splitext(self.split_f[1])
        err = (self.split_f[1] + '파일 받기 시작')
            print(err) 
            self.client_socket.sendall(err.encode('utf-8'))
        sed=Send.SendData(self.client,self.storage)
        if fileExtension == '.txt':
            Send.SendData.send_txt(self.split_f[1])
        elif fileExtension == '.png':
            Send.SendData.send_img(self.split_f[1]) 

        
        
        
        
        
            
            
            

      
