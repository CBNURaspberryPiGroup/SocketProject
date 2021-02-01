import socket
from PIL import Image

class RecvData:
    def __init__(self,client,storage):
        self.client = client
        self.stroage = storage
 
    def recv_img(self,fn):
        matadata= self.client.recv()
        matadata= matadata.split
        
        if len(matadata[1])==7 :
            matadata[1]=int(matadata[1][0:3]),int(matadata[1][4:])
             
        elif len(matadata[1])==8:
            if matadata[1]==",":
                matadata[1]=int(matadata[1][0:3]),int(matadata[1][4:])

            elif matadata[1][4]==",":
                matadata[1]=int(matadata[1][0:5]),int(matadata[1][5:])

        elif len(matadata[1])==9:
            matadata[1]=int(matadata[1][0:4]),int(matadata[1][5:])

        data=self.client.recv(1024)    
        data = Image.frombytes(matadata[1],matadata[3],data)
        Image.save(storage)