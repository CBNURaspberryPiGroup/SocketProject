import socket
from PIL import Image
import time 
import os

class RecvData:
    def __init__(self,client,storage):
        self.client = client
        self.storage = storage

    def recv_img(self,fn):
        matadata=self.client.recv(1024)
        matadata=matadata.decode()
        matadata= matadata.split(":")
        img_size= matadata[1].split(",")  
        size=tuple([int(img_size[0][1:]),int(img_size[1][1:-1])])
        img_mode=matadata[3]
        img_data=b""
        size=0
        start=time.time()
        while True:
            try:
                dat=self.client.recv(1024)
                size+=len(dat)
                img_data+=dat
                data=Image.frombytes(img_mode,size,img_data)
            except:
                pass            
            else:
                data.save("%s%s"%(self.storage,fn))
                break
        print("수신한 데이터:"+str(len)+"byte")
        print("소요시간:"+str(time.time()-start))   

    
    def recv_txt(self,fn):
        f=open("%s%s"%(self.storage,fn),'w')
        start=time.time()
        size=0
        while True :
            data=self.client.recv(1024)
            size+=len(data)
            print(data)
            if '\0' in data.decode():
                f.write(data.decode()[0:-1])
                break
            else :
                f.write(data.decode())
        print("수신한 데이터:"+str(len)+"byte")
        print("소요시간:"+str(time.time()-start))
            
            
            
            
        
