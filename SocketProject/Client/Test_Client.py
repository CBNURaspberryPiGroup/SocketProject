import socket
import os
import sys
import time
from PIL import Image




HOST = '203.227.140.199'  # The server's hostname or IP address
PORT = 9966        # The port used by the server

storage ='./'
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
print('서버와 연결되었습니다')
data = client.recv(1024)
print('파일',repr(data.decode()))
filename = input('받을 파일이름:')
client.sendall(filename.encode('utf-8'))

def split():
        split_f = filename.split(' ')  
        
        if split_f[0] == 'push':
            data = client.recv(1024)
            print(data.decode())
            file_push(split_f)
            
        elif split_f[0] == 'pull':
            data = client.recv(1024)
            print(data.decode())
            
            file_pull(split_f)
        
        else:
            data = client.recv(1024)
            print(data.decode())
            
                  
def file_pull(split_f):
    filename, fileExtension = os.path.splitext(split_f[1])
        
    if fileExtension == '.txt':
        f=open("%s%s"%(storage,split_f[1]),'w')
        data=""
        start =time.time()
        while not data=='\0'.encode():
            data=client.recv(1024)
            f.write(data.decode())
            if time.time()-start >=10:
                print(split_f[1]+ ' 받기실패 Timeout(10)')
                break    
        
        
    elif fileExtension == '.png'or '.jpg':
        try:
            
            matadata= client.recv(1024)
            matadata=matadata.decode()
            matadata= matadata.split(":")
            img_size= matadata[1].split(",")  # 여기까지 됨
            size=tuple([int(img_size[0][1:]),int(img_size[1][1:-1])])
            img_mode=matadata[3]
                 
            img_data=b""
            data = client.recv(1024)
            count=0 
            start =time.time()
            while True:
                count+=1 
                img_data+=data
                data=client.recv(1024)
                if time.time()-start >=10:
                    print(split_f[1]+ ' 받기실패 Timeout(10)')
                    break
            print(count)    
            
            img_data+=data

            data = Image.frombytes(img_mode,size,img_data) 
            
            data.save("%s%s"%(storage,split_f[1])) 
                

        except Exception as e:
            print(e)
            
           
        
def file_push(split_f):
    filename, fileExtension = os.path.splitext(split_f[1])
    print(fileExtension)
        
split()        
           
        
           
                
        




