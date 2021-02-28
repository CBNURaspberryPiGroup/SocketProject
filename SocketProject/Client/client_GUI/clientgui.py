
import PyQt5
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic , QtCore
import socket
import os
import sys
import time
from PIL import Image
import re
import json
import subprocess
from os.path import exists





                       


class sever_start(QThread): #돌아가는 서버ㄴㄹㄷ
    threadEvent = QtCore.pyqtSignal(str)
     
    def __init__(self,main):
        super().__init__()
        
        self.main = main
        self.isRun = False
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.storage = self.main.Storage
        self.n = ('안뇽')  
    
    def run(self):  #접속버튼 누르면 시작되는 부분
        
        self.main.json_rm() 
        try:
            self.client.connect((self.main.Host, int(self.main.Port)))
            self.n=('서버와 연결되었습니다')
            self.threadEvent.emit(self.n)
            
        except Exception as e:
                print(e)
                self.n=('서버 접속 실패 HOST,PORT 정보를 확인해주세요')
                self.threadEvent.emit(self.n)
                
                self.main.stop()
                return    
        self.main.btn_log.setEnabled(True)
        self.main.btn_log2.setEnabled(True)
        self.main.btn_sever.setEnabled(False)
        
    def run2(self):   #로그인이나 회원가입 성공하면 시작되는곳 
                
             
        
        self.main.btn_push.setEnabled(True)
        self.main.btn_pull.setEnabled(True)
        
        self.main.btn_log.setEnabled(False)
        self.main.btn_log2.setEnabled(False)
        
        print('ᕙ༼◕ ᴥ ◕༽ᕗ')
        data = self.client.recv(1024)
        data=data.decode()
        data = data.strip("[]")
        data = data.split(",")
        for i,k in enumerate(data) :
            if i == 0 : 
                self.main.listw.addItem(k[1:-1])
            else : 
                self.main.listw.addItem(k[2:-1])
        print('명령어 대기중')    
    
        
        
       
        
        
            
            
    
    def login(self):   #로그인 버튼 누르면 시작되는것
        self.client.sendall('y'.encode())
        if self.process(self.main.ID):
            if self.process(self.main.PW):
                self.n=('로그인 성공')
                self.threadEvent.emit(self.n)
                self.run2()
            
            
    def reg(self):  #회원가입 버튼 누르면 시작되는것
        self.client.sendall('n'.encode())  
        if self.process(self.main.ID):
            if self.process2(self.main.PW):
                data= self.client.recv(1024)
                self.n=(data.decode())
                
                self.threadEvent.emit(self.n)
                self.run2()
                   
    
    def process(self,inf):  #아이디 비번확인
        
        
            
        self.client.sendall(inf.encode())
        
        inf = self.client.recv(1024)
        inf = inf.decode()
        if inf == 'ID Not Found' or inf == 'Wrong Password' or inf == 'ID Already Exists': 
            self.n=(inf)
            self.threadEvent.emit(self.n)
            return False
        else:
            
            return True    
        
        
               
    
    
    
       
        
    def process2(self,inf) : #아이디 비번 확인2
            
               
                
        self.client.sendall(inf.encode())
        dnf = self.client.recv(1024)
        dnf = dnf.decode()
        print(dnf)
                
        self.client.sendall(inf.encode())
        if inf == 'Password Confirm Failed' :
            self.n=(inf)
            self.threadEvent.emit(self.n) 
            return False
        else:
            return True
           

     
    def sever_push(self):  #파일 업로드 누르면 시작
        filename =('push '+self.main.fn)
        
        
        self.split(filename)
        
        self.main.listw.clear()
        
        data = self.client.recv(1024)
        data=data.decode()
        data = data.strip("[]")
        data = data.split(",")
        for i,k in enumerate(data) :
            if i == 0 : 
                self.main.listw.addItem(k[1:-1])
            else : 
                self.main.listw.addItem(k[2:-1])
        print('명령어 대기중')
        
    def sever_pull(self):  #파일받기 누르면 시작
        filename =('pull '+self.main.fn)
        
        self.client.sendall(filename.encode('utf-8'))
        self.split(filename)
        self.main.listn.clear()
        self.main.list_show()
        print('명령어 대기중')
        
        
        
        
           
        

        
        
        
    

# 명령어 해석 ###############################################서버랑 같음

    def split(self,filename):
            split_f = filename.split(' ')  
            if split_f[0] == 'push':
                
                
                if exists (split_f[1]):
                    self.client.sendall(filename.encode('utf-8'))
                    de = self.client.recv(1024)
                    if de.decode() == 'not ok':
                        self.n=('파일이 이미 존재합니다') 
                        self.threadEvent.emit(self.n)
                        return
                    
                    self.file_push(split_f)
                    data = self.client.recv(1024)
                    self.n= data.decode()
                    self.threadEvent.emit(self.n)
                else:
                    self.client.sendall(b'no_file')
                    self.n=('파일이 존재하지 않습니다') 
                    self.threadEvent.emit(self.n)
                
                
            elif split_f[0] == 'pull':
                if self.no_file():
                    return
                if exists (split_f[1]):
                    self.n=('이미 존재하는 파일 입니다')
                    self.threadEvent.emit(self.n)
                    self.client.sendall(b'exists_file')
                    return
                self.client.sendall(b'ok')
                self.file_pull(split_f)
                self.main.list_show()
                pr= (split_f[1],'받기 완료')
                self.client.sendall(str(pr).encode())
                
            else:
                if self.no_file():
                    return
    
    def no_file(self):
        data = self.client.recv(1024)
        data= data.decode()
        if data == 'Error 이미 존재하는 파일입니다.' or data == 'Error 존재하지 않는 명령어 입니다' or data == 'Error 존재하지 않는 파일 입니다.':
            self.n= data
            self.threadEvent.emit(self.n)
            return True
      
            
                      
    # 파일 받기
                    
    def file_pull(self,split_f):
        filename, fileExtension = os.path.splitext(split_f[1])
            
        if fileExtension == '.txt':
            try:
                f=open("%s%s"%(self.storage,split_f[1]),'w')
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
                self.n =("수신한 데이터:"+str(size)+"byte")
                self.threadEvent.emit(self.n)
                
                self.n =("소요시간:"+str(time.time()-start)+"초")
                self.threadEvent.emit(self.n)
                self.n =('୧༼◕ ᴥ ◕༽୨')
                self.threadEvent.emit(self.n)
                       
            except Exception as e:
                print(e)               
            
            
        elif fileExtension == '.png'or fileExtension =='.jpg':
            try:
                
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
                        data.save("%s%s"%(self.storage,split_f[1]))
                        break
                self.n =("수신한 데이터:"+str(size)+"byte")
                self.threadEvent.emit(self.n)
                
                self.n =("소요시간:"+str(time.time()-start)+"초")
                self.threadEvent.emit(self.n)
                self.n =('୧༼◕ ᴥ ◕༽୨')
                self.threadEvent.emit(self.n)
                        

            except Exception as e:
                print(e)
            
        elif fileExtension == '.avi'or fileExtension == '.mp4' or fileExtension =='.mp3':
            try:
                vid=open(self.storage+'/'+split_f[1],"wb")       # tip: 각종 압축파일들은 용량을 줄이기 위해 바이너리화시킨다!
                a=0                                      # 수신한 데이터 크기를 표시하기 위한 변수a
                start=time.time()                        # time.time()은 현재시간-1970년 1월 1일 0시 0분 0초(유닉스 타임 시작 시기)를 초단위로 표현한것
               
                while True:                              
                    data=self.client.recv(1024)          
                    if data == b'\xeb\x81\x9d':
                        break
                                                    
                    a+=len(data)                          # a라는 변수에 수신한 data들의 크기를 더해주면서 최종 데이터의 크기를 함축한다.
                    vid.write(data)
                    
                self.n =("수신한 데이터:"+str(a)+"byte")
                self.threadEvent.emit(self.n)
                
                self.n =("소요시간:"+str(time.time()-start)+"초")
                self.threadEvent.emit(self.n)
                self.n =('୧༼◕ ᴥ ◕༽୨')
                self.threadEvent.emit(self.n)
                
                
            except Exception as e:
                print(e)    
                
                       
    # 파일 보내기
                
    def file_push(self,split_f):
        filename, fileExtension = os.path.splitext(split_f[1])
        if fileExtension == '.txt':
            self.send_txt(split_f)
            
        elif fileExtension == '.png'or fileExtension == '.jpg':
            self.send_img(split_f)    
        
        elif fileExtension == '.avi'or fileExtension == '.mp4' or fileExtension =='.mp3':
            self.send_vid(split_f)
        
    def send(self,data,size=1024):
            self.client.sendall(data)
            return len(data)
        
    def send_txt(self,split_f):
            try: 
                with open(self.storage+"/"+split_f[1],'r') as f:
                    data = f.readlines()
                
                size = 0
                for dat in data:
                    size += self.send(dat.encode())
                self.send('\0'.encode())
                return size
                
                self.n =('୧༼◕ ᴥ ◕༽୨')
                self.threadEvent.emit(self.n)
            except Exception as e:
                print(e)
                self.send(repr(e).encode())
                
    def send_img(self,split_f):
            try:
                data = Image.open(self.storage+"/"+split_f[1])
                # if '.jpg' in split_f[1][-4:] : modeConv = 'RGB'
                # elif '.png' in split_f[1][-4:] : modeConv = 'RGBA'
                # data = data.convert(mode=modeConv)
                metadata = "Size:%s:Mode:%s"%(data.size,data.mode)
                data = data.tobytes()
                self.send(metadata.encode())
                size = 0
                for i in range((len(data)-1)//1024+1):
                    print(i)
                    if len(data)-(i*1024) < 1024 :
                        size += self.send(data[i*1024:])
                        print('Last data N0.%s'%i)
                    else :
                        size += self.send(data[i*1024:(i+1)*1024])
                        print('data N0.%s'%i)
                        print(size)
                
                print('End')
                return size
            except Exception as e:
                print(e)
                self.send(repr(e).encode())
    
    def send_vid(self,split_f):
        vid=open(self.storage+"/"+split_f[1],"rb")
        for lines in vid.readlines():
            self.send(lines)
        time.sleep(1)    
        self.send('끝'.encode('utf-8')) 
        
            
################### GUI부분 ###############################################3       
            
class MainDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self, None)
        uic.loadUi("untitled.ui", self)
        
        with open('Setting.json','r', encoding='UTF-8') as fn:
            self.conf = json.load(fn)
        
        
        self.btn_sever.clicked.connect(self.start)
        self.btn_log2.clicked.connect(self.start2)
        self.btn_log.clicked.connect(self.start3)
        self.btn_push.clicked.connect(self.push)
        self.btn_pull.clicked.connect(self.pull)
        self.btn_stop.clicked.connect(self.stop)
        self.btn_f.clicked.connect(self.file_add)
        self.btn_push.setEnabled(False)
        self.btn_pull.setEnabled(False)
        self.btn_log.setEnabled(False)
        self.btn_log2.setEnabled(False)
        self.listn.itemDoubleClicked.connect(self.show_1)
        self.cb_ip.stateChanged.connect(self.rmip)
        self.cb_id.stateChanged.connect(self.rmid)
        self.cb_sto.stateChanged.connect(self.rmsto)
        self.cb_check()
        self.json_show()
        

        
    def file_add(self):  #찾기 버튼
        lm = dirname = QFileDialog.getExistingDirectory(self, self.tr("Open Data files"), "./", QFileDialog.ShowDirsOnly)
        if lm == '': return 0
        ref = re.compile('[ :a-zA-Z0-9_]+')
        splist = ref.findall(lm)
        lm = "\\".join(splist)+"\\"
        self.line_sto.setText(lm)    
        
    @pyqtSlot()    
    def start(self):   #접속버튼
          
        if self.check():
            if self.check_login():
                return
                
            if self.list_show():
                return
                    
            
            self.th = sever_start(self)
            self.th.threadEvent.connect(self.threadEventHandler)
            
                    
        
            self.textv.setPlainText('서버 접속 시도중...')
            
            if not self.th.isRun:
                print('메인 : 쓰레드 시작')
                self.th.isRun = True
                self.th.start()
        else:
            self.textv.append('입력정보가 올바른지 확인해주세요')
    
    def start2(self):
        ID = self.line_ed.text()
        self.ID =ID
        
        PW = self.line_pw.text()
        self.PW =PW  
          
        self.th.login()
        
    
    def start3(self):
        ID = self.line_ed.text()
        self.ID =ID
        
        PW = self.line_pw.text()
        self.PW =PW 
        
        self.th.reg()
    
    
    
                
    def check(self):   #미입력된 정보 체크하기 
        try:
            Host = self.line_ip.text()
            self.Host = Host
             
            
            Port = self.line_pt.text()
            self.Port =Port
         
            
            Storage = self.line_sto.text()
            self.Storage =Storage
           
                
            
            ID = self.line_ed.text()
            self.ID =ID
          
               
            
            
            PW = self.line_pw.text()
            self.PW =PW
            
                
        
            return True
        except Exception as e:
                print(e)
                return False
                  
    def check_login(self):
        
        if " " in self.ID : 
            self.textv.append("ID에 공백은 사용할 수 없습니다.")
            return True
        elif len(self.ID) >= 7 : 
            self.textv.append("ID를 7자 이하로 입력하세요")
            return True
        elif len(self.ID) <= 2: 
            self.textv.append("ID를 3자 이상 입력하세요")
            return True
        elif " " in self.PW : 
            self.textv.append("PW에 공백은 사용할 수 없습니다.")
            return True
        elif len(self.PW) >= 7 : 
            self.textv.append("PW를 7자 이하로 입력하세요")
            return True
        elif len(self.PW) <= 2: 
            self.textv.append("PW를 3자 이상 입력하세요") 
            return True
        else: return False                
        
    
    
            
    @pyqtSlot() 
    def push(self):    #업로드 버튼
        try:
            fn = self.listn.currentItem().text()
            self.fn =fn
            self.th.sever_push()
        except Exception as e:
            self.textv.append('업로드할 파일을 선택해주세요')
            print(e)    
            
        
        
    
    @pyqtSlot() 
    def pull(self):   #다운받기 버튼
        try:
            fn = self.listw.currentItem().text()
            print(fn)
            self.fn =fn
            self.th.sever_pull()
        except Exception as e:
            self.textv.append('다운받을 파일을 선택해주세요')
            print(e)
            
    
            
    @pyqtSlot()    
    def stop(self):    #접속 종료 버튼
        if self.th.isRun:
            print('메인 : 쓰레드 정지')
            self.th.isRun = False
            self.btn_push.setEnabled(False)
            self.btn_pull.setEnabled(False)
            self.btn_sever.setEnabled(True)
            self.btn_log.setEnabled(False)
            self.btn_log2.setEnabled(False)
            self.listn.clear()
            self.listw.clear()
            self.textv.clear()
            
        else:
            sys.exit()    
                
        
        
        
    @pyqtSlot(str)
    def threadEventHandler(self, n):
        print(n)
        self.textv.append(n)
    
    def show_1(self):
        print('더블클릭')
         
    #디렉토리 파일 보여주기       
    def list_show(self):
        try:   
            self.listn.clear()
            file_list1 = os.listdir(self.Storage)
            for file in file_list1: 
                if file.endswith(".txt") or file.endswith(".png") or file.endswith(".jpg") or file.endswith(".mp3") or file.endswith(".mp4") or file.endswith(".avi"):
                    self.listn.addItem(file)
            return False 
        except Exception as e:
            self.textv.append('Storage 정보가 맞는지 확인해주세요')
            print(e)  
            return True  
    #json 정보 불러오기        
    def json_show(self):
        
        
        self.line_ip.setText(self.conf['HOST']) 
        self.line_pt.setText(self.conf['PORT'])  
        self.line_sto.setText(self.conf['STORAGE'])  
        self.line_ed.setText(self.conf['ID'])
        
             
    #json에 정보 저장하기
    def json_rm(self):
        
        if self.rmip():
            self.conf['HOST']= self.line_ip.text()
            self.conf['PORT']= self.line_pt.text()
        
        else:
            self.conf['HOST']= ''
            self.conf['PORT']= ''
                
        
        if self.rmid():
            self.conf['ID']= self.line_ed.text()
            
        else:
            self.conf['ID'] =''
        
        if self.rmsto():
            self.conf['STORAGE']= self.line_sto.text()
        
        else:
            self.conf['STORAGE'] = ''
                
            
                
        with open('Setting.json','w', encoding='UTF-8')  as make_file:
            json.dump(self.conf, make_file, indent="\t")

                   

            
             
     #체크박스 값 받아오기         
    def rmip(self):  
        rm_ip = self.cb_ip.isChecked()
        return rm_ip
    
    def rmid(self):
        rm_id = self.cb_id.isChecked()
        return rm_id
    
    def rmsto(self):
        rm_sto = self.cb_sto.isChecked()
        return rm_sto    
    
    #json에 자장된 값이 있으면 체크박스 체크    
    def cb_check(self):  
        if self.conf['ID'] != '':
            self.cb_id.toggle()
                
        if self.conf['HOST'] != '':
            self.cb_ip.toggle() 
            
        if self.conf['STORAGE'] != '':
            self.cb_sto.toggle()     
        
        
if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        main_dialog = MainDialog()
       
        main_dialog.show()
    
        app.exec_()
    except Exception as e:
        print(e)        
        
        
        
        
        
        
        

        
           
        
           
                
        





