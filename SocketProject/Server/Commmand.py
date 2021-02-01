from socket import *
import os
from os.path import exists
import sys
import Send





class Command():
    
    def __init__(self,client,SendData):
        self.SendData = SendData
        self.sed = sed
        
        filename = self.clinet.recv(1024)
        
        self.filename = filename
        
        
    def split(self):
        self.split_f = self.filename.split(' ')  
        
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
                  
    def file_pull(self):
        fileExtension = os.path.splitext(self.split_f[1])[1]
        print(fileExtension)
        
        
        
        
        
            
            
            

              
    def file_push(self):
        filename, fileExtension = os.path.splitext(self.split_f[1])
        
        if fileExtension == '.txt':
            self.SendData.send_txt(self.split_f[1])
        elif fileExtension == '.png':
            self.SendData.send_img(self.split_f[1]) 

        
        
        
        
        
            
            
            

              
    def file_push(self):
        filename, fileExtension = os.path.splitext(self.split_f[1])
        
        if fileExtension == '.txt':
            self.SendData.send_txt(self.split_f[1])
        elif fileExtension == '.png':
            self.SendData.send_img(self.split_f[1]) 
      
