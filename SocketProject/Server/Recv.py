import socket
from PIL import Image

class RecvData:
    def __init__(self,client,storage):
        self.client = client
        self.stroage = storage

    def recv_img(self,fn):
        try:
            matadata= client.recv(1024)
            matadata=matadata.decode()
            matadata= matadata.split(":")
            img_size= matadata[1].split(",")  
            size=tuple([int(img_size[0][1:]),int(img_size[1][1:-1])])
            img_mode=matadata[3]

            if  fileExtension == '.png':
                data_len=int(img_size[0][1:])*int(img_size[1][1:-1])*4
                a=ceil(data_len/1024)
                img_data=b""
                for i in range(1:a+1):
                    data = client.recv(1024)
                    img_data+=data
                data = Image.frombytes(img_mode,size,img_data) 
                data.save("%s%s"%(storage,split_f[1]))
             
            
            elif  fileExtension == '.jpg':
                data_len=int(img_size[0][1:])*int(img_size[1][1:-1])*3
                a=ceil(data_len/1024)
                img_data=b""
                for i in range(1:a+1):
                    data = client.recv(1024)
                    img_data+=data
                data = Image.frombytes(img_mode,size,img_data) 
                data.save("%s%s"%(storage,split_f[1])) 

        except Exception as e:
            print(e)
            self.client.send(e)

    def recv_txt(self,fn):
        f=open("%s%s"%(storage,split_f[1]),'w')
         while True :
            data=client.recv(1024)
            if '\0'.decode() in data:
                f.write(data.decode()[0:-1])
                break
            else :
                f.write(data.decode())
            
            
        
