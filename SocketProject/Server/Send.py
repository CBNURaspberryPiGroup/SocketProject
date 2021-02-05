import socket
from PIL import Image 

class SendData:
    def __init__(self,client,storage):
        self.client = client
        self.storage = storage
        
    def send(self,data,size=1024):
        return self.client.sendall(data,size)

    def send_txt(self,fn):
        try: 
            with open(self.storage+"/"+fn,'r') as f:
                data = f.readlines()
            
            size = 0
            for dat in data:
                size += self.send(dat.encode())
            self.send('\0'.encode())
            return size
        except Exception as e:
            print(e.encode())
            self.send(repr(e).encode())

    def send_img(self,fn):
        try:
            data = Image.open(self.storage+"/"+fn)
            metadata = "Size|%s|Mode|%s"%(data.size,data.mode)
            data = data.tobytes()
            self.send(metadata)
            size = 0
            for i in range((len(data)-1)//1024+1):
                if (i+1)*1024-(i*1024) < 1024 :
                    size += self.send(data[i*1024:])
                else :
                    size += self.send(data[i*1024:(i+1)*1024])
            return size
        except Exception as e:
            print(e.encode())
            self.send(repr(e).encode())
