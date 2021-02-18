import socket
from PIL import Image

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
        while True:
            try:
                dat=self.client.recv(1024)
                img_data+=dat
                data=Image.frombytes(img_mode,size,img_data)
                result="ok"
            except:
                result="fail"
            if result=="ok":
                data.save("%s%s"%(self.storage,fn))
                break

    def recv_txt(self,fn):
        f=open("%s%s"%(self.storage,fn),'w')
        while True :
            data=self.client.recv(1024)
            if '\0' in data.decode():
                f.write(data.decode()[0:-1])
                break
            else :
                f.write(data.decode())     
            
            
        
