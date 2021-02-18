import socket
import os
import sys
import time
from PIL import Image

##################################################
#서버정보
HOST = '203.227.140.199'  # The server's hostname or IP address
PORT = 9966        # The port used by the server

#파일 보내거나 받을 주소
storage ='./'  
#######################################################3



# 디렉토리 파일 리스트
def list_f():
    file_list1 = os.listdir(storage)
        
        
    file_list =[]
    file_list.append([file for file in file_list1 if file.endswith(".txt")])
    file_list.append([file for file in file_list1 if file.endswith(".png")])
    file_list.append([file for file in file_list1 if file.endswith(".jpg")])

    print ('현제 디렉토리 파일: ',file_list)




# 명령어 해석

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
            
# 파일 받기
                  
def file_pull(split_f):
    filename, fileExtension = os.path.splitext(split_f[1])
        
    if fileExtension == '.txt':
        try:
            f=open("%s%s"%(storage,split_f[1]),'w')
            while True :
                data=client.recv(1024)
                if '\0' in data.decode():
                    f.write(data.decode()[0:-1])
                    print(split_f[1]+ '받기완료')
                    break
                else :
                    f.write(data.decode()) 
                    
        except Exception as e:
            print(e)               
        
        
    elif fileExtension == '.png'or '.jpg':
        try:
            
            matadata=client.recv(1024)
            matadata=matadata.decode()
            matadata= matadata.split(":")
            img_size= matadata[1].split(",")  
            size=tuple([int(img_size[0][1:]),int(img_size[1][1:-1])])
            img_mode=matadata[3]
            img_data=b""
            while True:
                try:
                    dat=client.recv(1024)
                    img_data+=dat
                    data=Image.frombytes(img_mode,size,img_data)
                    result="ok"
                except:
                    result="fail"
                if result=="ok":
                    data.save("%s%s"%(storage,fn))
                    break    

        except Exception as e:
            print(e)
            
# 파일 보내기
            
def file_push(split_f):
    filename, fileExtension = os.path.splitext(split_f[1])
    if fileExtension == '.txt':
        send_txt(split_f)
        
    elif fileExtension == '.png'or '.jpg':
        send_img(split_f)    
    
def send(data,size=1024):
        client.sendall(data,size)
        return len(data)
    
def send_txt(split_f):
        try: 
            with open(storage+"/"+split_f[1],'r') as f:
                data = f.readlines()
            
            size = 0
            for dat in data:
                size += send(dat.encode())
            send('\0'.encode())
            return size
            
        except Exception as e:
            print(e)
            send(repr(e).encode())
            
def send_img(split_f):
        try:
            data = Image.open(storage+"/"+split_f[1])
            metadata = "Size:%s:Mode:%s"%(data.size,data.mode)
            data = data.tobytes()
            send(metadata.encode())
            size = 0
            for i in range((len(data)-1)//1024+1):
                print(i)
                if len(data)-(i*1024) < 1024 :
                    size += send(data[i*1024:])
                    print('Last data N0.%s'%i)
                else :
                    size += send(data[i*1024:(i+1)*1024])
                    print('data N0.%s'%i)
                    print(size)
            send('\0'.encode())
            print('End')
            return size
        except Exception as e:
            print(e)
            send(repr(e).encode())                       
        


def Id_login ():
        id = client.recv(1024)
        Deid = id.decode()
        print("ID를 입력하세요.")
        
        while True :
            ID = input(Deid)
            # ID_list = ID.split()
            if " " in ID : print("공백은 사용할 수 없습니다.")
                
            elif len(ID) >= 8 : print("ID는 8자 이하로 입력하세요")
                
            elif len(ID) <= 3: print("ID는 3자 이상 입력하세요")
                
            else : False
        print("ID 처리 완료")
        client.sendall(ID.encode)

def pw_login():
    pw = client.recv(1024)
    depw = pw.decode()
    print("pw를 입력하세요.")
            
    while True :
        pw = input(depw)
        
        if " " in pw: 
            print("공백은 사용 할 수 없습니다.")
            
        elif len(pw) >= 8: 
            print("pw는 8자 이하로 입력하세요")
            
        elif len(pw) <= 3: 
            print("pw는 3자 이상 입력하세요")
            
        else : 
            False
        print("pw 처리 완료")
        client.sendall(pw.encode())

def split2(se):
    if se == 'y':
        Id_login()
        pw_login()
    if se == 'n':
        pass    
    else:
        sys.exit()


## 가동 ##

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
print('서버와 연결되었습니다')
print('ᕙ༼◕ ᴥ ◕༽ᕗ')
logein =input('로그인을할려면 y 회원가입을 할려면 n 을 입력하세요:')
client.sendall(logein.encode())
split2(logein)














data = client.recv(1024)
print('서버에 있는 파일',repr(data.decode()))
print('୧༼◕ ᴥ ◕༽୨')
list_f()
print('ᕙ༼◕ ᴥ ◕༽ᕗ')
print('서버에서 파일을 받고 싶으면 pull, 업로드 하고싶을면 push르 입력후 파일명을 입력하십시오')
print('୧༼◕ ᴥ ◕༽୨')
filename = input('명령어 파일명:')
client.sendall(filename.encode('utf-8'))
split()
