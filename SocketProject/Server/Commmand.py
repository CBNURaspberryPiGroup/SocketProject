from socket import *
import os
from os.path import exists
import sys
import Send
import Recv
import Identification
import Logging as Log




class Command():
    
    def __init__(self,client,storage):
        
        self.storage = storage
        self.client = client
       
        
        
    def split(self):
        filename = self.client.recv(1024)
        print(filename)
        filename = filename.decode().replace("\0","")
        print(filename)
        self.split_f = filename.split(' ')  
        
        if self.split_f[0] == 'push':
            if exists(self.split_f[1]):
               
                self.client.sendall('Error 이미 존재하는 파일입니다.'.encode('utf-8'))
                
                print('Error 이미 존재하는 파일입니다.')
            else:
                if self.client.recv(1024) ==  b'no_file':
                    print('Error 클라이언트에 존재하지 않는 파일')
                    pass
                else:  
                    self.file_push()
            
        elif self.split_f[0] == 'pull':
            if not exists(self.split_f[1]):
                
                self.client.sendall('Error 존재하지 않는 파일 입니다.'.encode('utf-8'))
                
                print('Error 존재하지 않는 파일 입니다.')
            else:
                if self.client.recv(1024) ==  b'exists_file':
                    print('Error 클라이언트에 이미 존재하는 파일')
                    pass    
                else:
                    self.file_pull()
        
        else:
            
            print('Error 존재하지 않는 명령어 입니다') 
            Log.log(0,"Invalid Command : %s"%filename)
            self.client.sendall('Error 존재하지 않는 명령어 입니다'.encode('utf-8'))
    
    def split2(self):
        id=Identification.Identification(self.client)
        while True:
            logein = self.client.recv(1024)
            logein = logein.decode()
            


            if logein == 'y':
                print('y')
                if id.Authentification():
                    break

            if logein == 'n':
                print('n')
                if id.Register():
                    break
            
            
            
        
    
    
                  
    def file_push(self):
        filename, fileExtension = os.path.splitext(self.split_f[1])
        err = (self.split_f[1] + '파일 업로드 시작')
        print(err) 
        self.client.sendall(err.encode('utf-8'))
        Rec=Recv.RecvData(self.client,self.storage)
        if fileExtension == '.txt':
            Rec.recv_txt(self.split_f[1])
        elif fileExtension == '.png'or'.jpg':
            Rec.recv_img(self.split_f[1])
        elif fileExtension == '.avi'or'.mp4' or'.mp3':
            Rec.recv_vid(self.split_f[1])  
        
              
    def file_pull(self):
        filename, fileExtension = os.path.splitext(self.split_f[1])
        err = (self.split_f[1] + '파일 받기 시작')
        print(err) 
        self.client.sendall(err.encode('utf-8'))
        sed=Send.SendData(self.client,self.storage)
        if fileExtension == '.txt':
            sed.send_txt(self.split_f[1])
            data = self.client.recv(1024)
            print(data.decode())
        elif fileExtension == '.png'or'.jpg':
            sed.send_img(self.split_f[1])
            data = self.client.recv(1024)
            print(data.decode())
                
        elif fileExtension == '.avi'or'.mp4' or'.mp3':
            sed.send_vid(self.split_f[1])
            data=self.client.recv(1024)
            print(data.decode())
