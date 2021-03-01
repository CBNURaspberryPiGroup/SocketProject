import socket
from PIL import Image
import time 
import os
import work

class RecvData:                                  # 통신을 할 때는 통일성을 위해 보내는 정보를 아스키코드로 변환시킨뒤(encode함수 이용) 보내기로 약속했다.(세계 규약)
    def __init__(self,client,storage):           
        self.client = client
        self.storage = storage
                                                 # "wb"는 바이너리 파일을 작성모드로 열기위한 모드이다!
    def recv_vid(self,fn):                       # 각종 바이너리 파일(mp4,mp3,avi)들은 각 파일에 프레임마다 바이너리화된 문자열(그 프레임의 원시데이터)가 존재
        vid=open(self.storage+'/'+fn,"wb")       # tip: 각종 압축파일들은 용량을 줄이기 위해 바이너리화시킨다!
        a=0                                      # 수신한 데이터 크기를 표시하기 위한 변수a
        start=time.time()                        # time.time()은 현재시간-1970년 1월 1일 0시 0분 0초(유닉스 타임 시작 시기)를 초단위로 표현한것

        while True:                              #'\xeb\x81\x9d'는 "끝"을 유니코드로 변환한것 즉 send.py에서 "끝"이라는 문자열이 올때까지 데이터를 계속 받은 뒤 
            data=self.client.recv(1024)          # vid 파일에 받은 데이터(받을 파일을 구성하고 있는 문자열)를 작성시킨다. 받은 모든 데이터가 다 작성되면 그 파일이 정상적으로 실행된다.
            if data == b'\xeb\x81\x9d':
                break
            a+=len(data)                                 # a라는 변수에 수신한 data들의 크기를 더해주면서 최종 데이터의 크기를 함축한다.
            vid.write(data)

        print("수신한 데이터:"+str(a)+"byte")     # 수신한 데이터 표시 
        print("소요시간:"+str(time.time()-start)+"초")  # 현재시간에 시작시간을 빼서 소요시간 표시
        print('୧༼◕ ᴥ ◕༽୨')
        wok=work.filelist(self.client,self.storage)    
        wok.list_f()    
                 
    '''def recv_img(self,fn):
        matadata=self.client.recv(1024)          # 메타데이터는 이미지의 모드(ex) rgb,rgba 등등)와 이미지의 사이즈(ex) 1024x1024 등등)의 정보를 나타낸다. send.py에서 각 정보를 추출하여 보내준다.
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
                dat=self.client.recv(1024)       # frombytes함수는 이미지를 합성시킬 때 필요한 데이터가 충족되지 않으면 오류를 보내는데 try구문을 이용하여 이미지가 합성될 때까지 데이터를 계속받는다.
                a+=len(dat)
                img_data+=dat
                data=Image.frombytes(img_mode,size,img_data)
            except:
                pass            
            else:
                data.save("%s%s"%(self.storage,fn))    # 합성한 이미지를 저장한다.
                break
        print("수신한 데이터:"+str(a)+"byte")
        print("소요시간:"+str(time.time()-start)+"초")
        print('୧༼◕ ᴥ ◕༽୨')
        wok=work.filelist(self.client,self.storage)    # work함수에서 현 디렉토리내의 파일들을 서버측에 보내준다.
        wok.list_f()'''

    
    def recv_txt(self,fn):
        f=open("%s%s"%(self.storage,fn),'w')          # 받을 텍스트 파일을 저장하기 위해 open사용
        start=time.time()
        size=0
        while True :
            data=self.client.recv(1024)               # send.py에서 보낼txt파일의 각 문장들을 readlines함수를 이용해 보내줌
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
        wok=work.filelist(self.client,self.storage)
        wok.list_f()
            
            
            
            
        
