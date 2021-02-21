import socket
from PIL import Image
import time 
import os
import work
import Commmand

class RecvData:
    def __init__(self,client,storage):
        self.client = client
        self.storage = storage
    '''def recv(self,size=1024):
        try:
            self.client.recv(1024)
        except ConnectionResetError:
            print("연결이 끊어졌습니다.")
            a=0
            while True :
                a += 1
                Host=input("ip값을 입력해주세요")
                Port=input("port값을 입력해주세요")
                self.client.bind((Host,Port))
                print("listening...")
                self.client.listen()
                print("listened")
                client, addr = self.client.accept()
                print('Connected by '+str(addr))
                Com = Commmand.Command(self.client,self.storage)
                if a == 1 : 
                    Com.split2()
                wok=work.filelist(self.client,self.storage)
                wok.list_f()
                Com.split()'''
                 
    def recv_img(self,fn):
        matadata=self.client.recv(1024)
        matadata=matadata.decode()
        matadata= matadata.split(":")
        img_size= matadata[1].split(",")  
        size=tuple([int(img_size[0][1:]),int(img_size[1][1:-1])])
        img_mode=matadata[3]
        img_data=b""
        a=0
        start=time.time()
        while True:
            try:
                dat=self.client.recv(1024)
                a+=len(dat)
                img_data+=dat
                data=Image.frombytes(img_mode,size,img_data)
            except:
                pass            
            else:
                data.save("%s%s"%(self.storage,fn))
                break
        print("수신한 데이터:"+str(a)+"byte")
        print("소요시간:"+str(time.time()-start)+"초")
        print('୧༼◕ ᴥ ◕༽୨')
        wok=work.filelist(self.client,self.storage)
        wok.list_f()

    
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
        print("수신한 데이터:"+str(size)+"byte")
        print("소요시간:"+str(time.time()-start)+"초")
        print('୧༼◕ ᴥ ◕༽୨')
        wok=work.filelist(self.client,self.storage)
        wok.list_f()
            
            
            
        
