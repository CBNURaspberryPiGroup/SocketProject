import socket
from PIL import Image

class RecvData:
    def __init__(self,client,storage):
        self.client = client
        self.stroage = storage

    def recv_img(self,fn):
        try:
            matadata= self.client.recv()
            matadata= matadata.split("|")
            img_size= matadata[1].split(",")
            size="%i,%i" %img_size[1][1:] %img_size[2][1:]
        
            img_mode=matadata[3]
        
            img_data=""
            data = self.client.recv(1024) 
            while len(data)==1024 : 
                img_data+=data
                data=self.client.recv(1024)
            data=self.cliemt.recv(1024)
            img_data+=data

            data = Image.frombytes(size,img_mode,img_data) #(size,mode,data)
            data.save("%s/+fn") % self.stroage

        except Exception as e:
            print(e)
            self.client.send(e)

    def recv_txt(self,fn)
         try:
            f=open("cliet.stroage+fn",'w')
            while True:
            data=self.client.recv()
            f.write(data)
            
            except Exception as e:
            print(e)
            self.send(e)

