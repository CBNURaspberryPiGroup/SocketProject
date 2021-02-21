
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






                       


class sever_start(QThread): #돌아가는 서버
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
        
    
        
        
       
        
        
            
            
    
    def login(self):   #로그인 버튼 누르면 시작되는것
        self.client.sendall('y'.encode())
        if self.process(self.main.ID):
            if self.process(self.main.PW):
                self.run2()
            
            
    def reg(self):  #회원가입 버튼 누르면 시작되는것
        self.client.sendall('n'.encode())  
        if self.process(self.main.ID):
            if self.process2(self.main.PW):
                data= self.client.recv(1024)
                self.n=(data.decode())
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
        self.client.sendall(filename.encode('utf-8')) 
        
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
        
        
    def sever_pull(self):  #파일받기 누르면 시작
        filename =('pull '+self.main.fn)
        self.client.sendall(filename.encode('utf-8'))
        
        self.split(filename)
        self.main.listn.clear()
        self.main.list_show()
        
        
        
        
        
           
        

        
        
        
    

# 명령어 해석 ###############################################서버랑 같음

    def split(self,filename):
            split_f = filename.split(' ')  
            if split_f[0] == 'push':
                print(split_f[0])
                data = self.client.recv(1024)  #문제발생
                print(data.decode())
                self.file_push(split_f)
                
                
            elif split_f[0] == 'pull':
                data = self.client.recv(1024)
                print(data.decode())
                
                self.file_pull(split_f)
                
            else:
                data = self.client.recv(1024)
                print(data.decode())
                
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
                print("수신한 데이터:"+str(size)+"byte")
                print("소요시간:"+str(time.time()-start)+"초")
                print('୧༼◕ ᴥ ◕༽୨')
               
                       
            except Exception as e:
                print(e)               
            
            
        elif fileExtension == '.png'or '.jpg':
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
                print("수신한 데이터:"+str(a)+"byte")
                print("소요시간:"+str(time.time()-start)+"초")
                print('୧༼◕ ᴥ ◕༽୨')
                        

            except Exception as e:
                print(e)
                
    # 파일 보내기
                
    def file_push(self,split_f):
        filename, fileExtension = os.path.splitext(split_f[1])
        if fileExtension == '.txt':
            self.send_txt(split_f)
            
        elif fileExtension == '.png'or '.jpg':
            self.send_img(split_f)    
        
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
            except Exception as e:
                print(e)
                self.send(repr(e).encode())
                
    def send_img(self,split_f):
            try:
                data = Image.open(self.storage+"/"+split_f[1])
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
                self.send('\0'.encode())
                print('End')
                return size
            except Exception as e:
                print(e)
                self.send(repr(e).encode())        
              
        
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
                if file.endswith(".txt") or file.endswith(".png") or file.endswith(".jpg"):
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
        
        
        
        
        
        
        

        
           
        
           
                
        





