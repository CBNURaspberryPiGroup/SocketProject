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
    file_list.append([file for file in file_list1 if file.endswith(".avi")])
    file_list.append([file for file in file_list1 if file.endswith(".mp4")])
    file_list.append([file for file in file_list1 if file.endswith(".mp3")])


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
                    data.save("%s%s"%(storage,split_f[1]))
                break    

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
        client.sendall(data,size)
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
            send('\0'.encode())
            print('End')
            return size
        except Exception as e:
            print(e)
            send(repr(e).encode())                       
        
 
def reg() :
    def condition (inf) :
            while True :
                inf = input(inf)
                if " " in inf : print("공백은 사용할 수 없습니다.")
                elif len(inf) >= 7 : print("ID는 7자 이하로 입력하세요")
                elif len(inf) <= 2: print("ID는 3자 이상 입력하세요")                
                else : break
    
    def ID_process (inf) : # ID / log in + sign up for 
        while True :
            inf = client.recv(1024)
            inf = inf.decode()
            condition(inf)
            client.sendall(inf.encode())
            inf = client.recv(1024)
            inf = inf.decode()
            # inf = client.recv(1024)
            # inf = inf.decode()
            if inf == 'ID Already Exists' :
                print(inf)
            else : break
       
     
    def pw_process2 (inf) : # PW / log in + sign up for id
        while True :
            inf = client.recv(1024)
            inf = inf.decode()
            condition(inf)
            client.sendall(inf.encode()) #PW send
            inf = client.recv(1024)
            inf = inf.decode()
            condition(inf)
            client.sendall(inf.encode()) # Pw confirm
            inf = client.recv(1024)
            inf = inf.decode()
            if inf == 'Password Confirm Failed' : print(inf)
            else : break
        
    id = ""
    pw = ""
    ID_process(id)
    pw_process2(pw)

def login ():
    def condition (inf) :
            while True :
                inf = input(inf)
                if " " in inf : print("공백은 사용할 수 없습니다.")
                elif len(inf) >= 7 : print("ID는 7자 이하로 입력하세요")
                elif len(inf) <= 2: print("ID는 3자 이상 입력하세요")                
                else : break
    
    def ID_process (inf) :
        while True :
            inf = client.recv(1024)
            inf = inf.decode()
            condition(inf)
            client.sendall(inf.encode())
            inf = client.recv(1024)
            inf = inf.decode()
            if inf == 'ID Not Found' : print(inf)
            else : break
        

    def pw_process (inf) :
        while True :
            inf = client.recv(1024)
            inf = inf.decode()
            condition(inf)
            client.sendall(inf.encode())
            inf = client.recv(1024)
            inf = inf.decode()
            if inf == 'Wrong Password' : print(inf)
            else : break
        
    id = ""
    pw = ""
    ID_process(id)
    pw_process(pw)



    
        

def split2(se):
    if se == 'y':
        login()
    if se == 'n':
        reg()
        time.sleep(1)
        sys.exit()
    else:
        sys.exit()

a = 0
## 가동 ##
while 1 :
    a += 1
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    if a == 1 :
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
