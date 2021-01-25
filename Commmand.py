from socket import *
import os
from os.path import exists
import sys


# serverSock = socket(AF_INET, SOCK_STREAM)
# serverSock.bind(('', 9966))
# serverSock.listen(1)
# print('listening....')
# connectionSock, addr = serverSock.accept()


class Command():
    
    def __init__(self):
        super().__init__()
        
        # filename = connectionSock.recv(1024)
        filename = 'pull wlans.txt'
        self.filename = filename
        self.split()
        
    def split(self):
        split_f = self.filename.split(' ')  
        
        if split_f[0] == 'push':
            if not exists(split_f[1]):
                err = ('Error -'+split_f[1]+'- 존재하지 않는 파일 입니다') 
                # connectionSock.sendall(err.encode('utf-8'))
                # Command()
                print(err)
            else:    
                self.file_push()
            
        elif split_f[0] == 'pull':
            if not exists(split_f[1]):
                err = ('Error -'+split_f[1]+'- 존재하지 않는 파일 입니다') 
                # connectionSock.sendall(err.encode('utf-8'))
                # Command() 
                print(err)
            else:    
                self.file_pull()
        
        else:
            err = ('Error -'+split_f[0]+'- 존재하지 않는 명령어 입니다')
            print(err) 
            # connectionSock.sendall(err.encode('utf-8'))
                  
    def file_pull(self):
        print('pull')
              
    def file_push(self):
        print('push')
            
Command()       