import socket
import os
import sys
import time
from os.path import exists
from PIL import Image

##################################################
#서버정보
HOST = '1.246.117.24'  # The server's hostname or IP address
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
    file_list.append([file for file in file_list1 if file.endswith(".avi")])
    file_list.append([file for file in file_list1 if file.endswith(".mp4")])
    file_list.append([file for file in file_list1 if file.endswith(".mp3")])
    return file_list
    






# 명령어 해석

def split():
        split_f = filename.split(' ')  
        
        if split_f[0] == 'push':
            if exists (split_f[1]):
                file_push(split_f)
                data = client.recv(1024)
                print(data.decode())
            else:
                client.sendall(b'no_file')
                print('파일이 존재하지 않습니다')   
            
        elif split_f[0] == 'pull':
            if no_file():
                return
            if exists (split_f[1]):
                print('이미 존재하는 파일 입니다')
                client.sendall(b'exists_file')
                return
        
            file_pull(split_f)
            
            file_list=str(list_f())
            client.sendall(file_list.encode())
            
        
        else:
            if no_file():
                return


def no_file():
    data = client.recv(1024)
    data= data.decode()
    if data == '이미 존재하는 파일입니다.' or data == 'Error 존재하지 않는 명령어 입니다' or data == 'Error 존재하지 않는 파일 입니다.':
        print(data)
        return True
    else:
        print(data)        
    
    
            
# 파일 받기
                  
def file_pull(split_f):
    filename, fileExtension = os.path.splitext(split_f[1])
        
    if fileExtension == '.txt':
        try:
            f=open("%s%s"%(storage,split_f[1]),'w')          # 받을 텍스트 파일을 저장하기 위해 open사용
            start=time.time()
            size=0
            while True :
                data=client.recv(1024)               # send.py에서 보낼txt파일의 각 문장들을 readlines함수를 이용해 보내줌
                size+=len(data)                           
                print(data)
                if '\0' in data.decode():                 # 텍스트 파일은 바이너리 파일이 아니기 때문에 텍스트 상에 null('\0'.decode())문자가 포함되지 않는다. 
                    f.write(data.decode()[0:-1])          # 이를 이용하여 send.py에서는 텍스트파일의 각 문장들을 다보낸뒤 마침을 알리고자 null문자를 보내고
                    break                                 # 수신측에서는 null문자가 오면 마지막 문장에서 null문자를  뺀뒤 저장한다.
                else :
                    f.write(data.decode())               
            print("수신한 데이터:"+str(size)+"byte")
            print("소요시간:"+str(time.time()-start)+"초")
            print('୧༼◕ ᴥ ◕༽୨')
                    
        except Exception as e:
            print(e)               
        
        
    elif fileExtension == '.png'or '.jpg':
        try:
            
            matadata=client.recv(1024)          # 메타데이터는 이미지의 모드(ex) rgb,rgba 등등)와 이미지의 사이즈(ex) 1024x1024 등등)의 정보를 나타낸다. send.py에서 각 정보를 추출하여 보내준다.
            matadata=matadata.decode()               # 받은 메타데이터를 디코딩해준다.
            matadata= matadata.split(":")            # 메타데이터는 "Size:%s:Mode:%s"%(data.size,data.mode)의 형식으로 오는데 이 값들(%s)을 추출하기 위해 스플릿한다.
            img_size= matadata[1].split(",")         # matadata[1]="1231,1213"로 사이즈를 의미하는데 이를,로 스플릿 한다.         
            size=tuple([int(img_size[0][1:]),int(img_size[1][1:-1])]) # 받을 각정보들을 frombytes함수를 이용하여 재합성 시킬 때 사이즈 인수는 튜플로 받기 때문에 옆과 같은 과정을 거친다.""
            img_mode=matadata[3]                     # 이미지의 모드 정보를 의미한다. 
            img_data=b""                             # 이미지를 send.py에서 tobytes함수로 이미지의 원시데이터를 추출하는데 이를 받기 위한 인수이다.
            a=0
            start=time.time()   
            while True:
                try:
                    dat=client.recv(1024)       # frombytes함수는 이미지를 합성시킬 때 필요한 데이터가 충족되지 않으면 오류를 보내는데 try구문을 이용하여 이미지가 합성될 때까지 데이터를 계속받는다.
                    a+=len(dat)
                    img_data+=dat
                    data=Image.frombytes(img_mode,size,img_data)
                except:
                    pass            
                else:
                    data.save("%s%s"%(storage,split_f[1]))    # 합성한 이미지를 저장한다.
                    break
            print("수신한 데이터:"+str(a)+"byte")
            print("소요시간:"+str(time.time()-start)+"초")
            print('୧༼◕ ᴥ ◕༽୨')   

        except Exception as e:
            print(e)
            
    elif fileExtension == '.avi'or '.mp4' or '.mp3':
        try:
            vid=open(storage+'/'+split_f[1],"wb")
            a=0
            start=time.time()

            while True:
                data=client.recv(1024)
                if data==b'\xeb\x81\x9d':
                    break
                vid.write(data)
            print("수신한 데이터:"+str(a)+"byte")
            print("소요시간:"+str(time.time()-start)+"초")
            print('୧༼◕ ᴥ ◕༽୨')
        except Exception as e:
            print(e)    

# 파일 보내기
            
def file_push(split_f):
    filename, fileExtension = os.path.splitext(split_f[1])
    if fileExtension == '.txt':
        send_txt(split_f)
        
    elif fileExtension == '.png'or '.jpg':
        send_img(split_f)
    elif fileExtension == '.avi'or '.mp4'or'.mp3':
        send_vid(split_f)    
    
def send(data,size=1024):
        client.sendall(data)
        return len(data)

def send_vid(split_f):
    try:
        vid=open(storage+"/"+split_f[1],"wb")
        for lines in vid.readlines():
            send(lines)
        send('끝'.encode('utf-8')) 
    except Exception as e:
        print(e)
        send(repr(e).encode())
    
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
            
            print('End')
            return size
        except Exception as e:
            print(e)
            send(repr(e).encode())                       
        
class login3():
    def __init__(self,client):
        self.client = client
        
        
         
    def login(self):   #로그인 버튼 누르면 시작되는것
            self.client.sendall('y'.encode())
            if self.process(input('ID:')):
                if self.process(input('PW:')):
                    return True
            
            
    def reg(self):  #회원가입 버튼 누르면 시작되는것
        self.client.sendall('n'.encode())  
        if self.process(input('ID:')):
            if self.process2(input('PW:')):
                
                return True
                
                   
    
    def process(self,inf):  #아이디 비번확인
        
        
            
        self.client.sendall(inf.encode())
        
        inf = self.client.recv(1024)
        inf = inf.decode()
        if inf == 'ID Not Found' or inf == 'Wrong Password' or inf == 'ID Already Exists': 
            print(inf)
            return False
        else:
            print(inf)
            return True    
        
        
               
    
    
    
       
        
    def process2(self,inf) : #아이디 비번 확인2
            
               
                
        self.client.sendall(inf.encode())
        dnf = self.client.recv(1024)
        dnf = dnf.decode()
        
                
        self.client.sendall(input(dnf).encode())
        inf = self.client.recv(1024)
        inf = inf.decode()
        if inf == 'Password Confirm Failed' :
            print(inf) 
            return False
        else:
            print(inf)
            return True
           



    
        

    def split2(self,se):
        if se == 'y':
            if self.login():
                return True
            
        if se == 'n':
            if self.reg():
                return True
            
       

a = 0
## 가동 ##
try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    while 1 :
        a += 1
        if a == 1 :
            re=login3(client)
            print('서버와 연결되었습니다')
            print('ᕙ༼◕ ᴥ ◕༽ᕗ')
            while True:
                if re.split2(input('로그인을 할려면 y, 화원가입을 할려면 n 을 입력하세요:')):
                    break
               
        data = client.recv(1024)
        print('서버에 있는 파일',repr(data.decode()))
        print('')
        
        print ('현제 디렉토리 파일: ',list_f())
        print('')
        print('서버에서 파일을 받고 싶으면 pull, 업로드 하고싶을면 push를 입력후 파일명을 입력하십시오')
        print('')
        filename = input('명령어 파일명:')
        client.sendall(filename.encode('utf-8'))
        split()
except Exception as e:
    print(e)
