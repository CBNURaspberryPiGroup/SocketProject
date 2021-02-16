
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





# 디렉토리 파일 리스트
                       


class sever_start(QThread):
    threadEvent = QtCore.pyqtSignal(str)
     
    def __init__(self,main):
        super().__init__()
        
        self.main = main
        self.isRun = False
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.storage = self.main.Storage
        self.n = ('안뇽')  
    
    def run(self):
        
        self.main.json_rm() 
        
        self.main.client.connect((self.main.Host, int(self.main.Port))) 
        self.n = ('서버와 연결되었습니다')
        
        self.threadEvent.emit(self.n)
        self.main.btn_push.setEnabled(True)
        self.main.btn_pull.setEnabled(True)
        self.main.btn_sever.setEnabled(False)
        
        print('ᕙ༼◕ ᴥ ◕༽ᕗ')
        data = client.recv(1024)
        for path in data.decode():
            self.lsitw.addItem(path)
            
           
            
    def sever_push(self):  #확인
        filename =('push '+self.main.fn)
        self.client.sendall(filename.encode('utf-8')) 
        
        sev=sever()
        sev.split(filename)
        
    def sever_pull(self):
        filename =('pull ',self.main.fn)
        self.client.sendall(filename.encode('utf-8'))
        
        sev=sever()
        sev.split(filename)
           
        
class sever():
    def __intit__(self,sever_start):
        
        self.sever_start = sever_start
        
        
        
    

# 명령어 해석

    def split(self,filename):
            split_f = filename.split(' ')  
            if split_f[0] == 'push':
                print(split_f[0])
                data = self.sever_start.client.recv(1024)  #문제발생
                print(data.decode())
                file_push(split_f)
                
                
            elif split_f[0] == 'pull':
                data = self.sever_start.client.recv(1024)
                print(data.decode())
                
                file_pull(split_f)
                
            else:
                data = self.sever_start.client.recv(1024)
                print(data.decode())
                
    # 파일 받기
                    
    def file_pull(self,split_f):
        filename, fileExtension = os.path.splitext(split_f[1])
            
        if fileExtension == '.txt':
            try:
                f=open("%s%s"%(self.sever_start.storage,split_f[1]),'w')
                while True :
                    data=self.sever_start.client.recv(1024)
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
                
                matadata= self.sever_start.client.recv(1024)
                matadata=matadata.decode()
                print(matadata)
                matadata= matadata.split(":")
                img_size= matadata[1].split(",")  # 여기까지 됨
                size=tuple([int(img_size[0][1:]),int(img_size[1][1:-1])])
                img_mode=matadata[3]
                    
                img_data=b""
                data = self.sever_start.client.recv(1024)
                count=0 
                start =time.time()
                while True:
                    count+=1 
                    img_data+=data
                    data=self.sever_start.client.recv(1024)
                    if time.time()-start >=10:
                        print(split_f[1]+ ' 받기실패 Timeout(10)')
                        break
                print(count)    
                
                img_data+=data

                data = Image.frombytes(img_mode,size,img_data) 
                
                data.save("%s%s"%(self.main.storage,split_f[1])) 
                    

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
            self.sever_start.client.sendall(data,size)
            return len(data)
        
    def send_txt(self,split_f):
            try: 
                with open(self.main.storage+"/"+split_f[1],'r') as f:
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
                data = Image.open(self.sever_start.storage+"/"+split_f[1])
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
              
        
        
            
class MainDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self, None)
        uic.loadUi("untitled.ui", self)
        
        with open('Setting.json','r', encoding='UTF-8') as fn:
            self.conf = json.load(fn)
        
        
        self.btn_sever.clicked.connect(self.start)
        self.btn_push.clicked.connect(self.push)
        self.btn_pull.clicked.connect(self.pull)
        self.btn_stop.clicked.connect(self.stop)
        self.btn_f.clicked.connect(self.file_add)
        self.btn_push.setEnabled(False)
        self.btn_pull.setEnabled(False)
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
            self.list_show() 
            self.th = sever_start(self)
            self.th.threadEvent.connect(self.threadEventHandler)
            
                    
        
            self.textv.append('서버 접속 시도중...')
            
            if not self.th.isRun:
                print('메인 : 쓰레드 시작')
                self.th.isRun = True
                self.th.start()
        else:
            self.textv.append('입력정보가 올바른지 확인해주세요')
                
    def check(self):   #미입력된 정보 체크하기 
        try:
            Host = self.line_ip.text()
            
            self.Host = Host
            Port = self.line_pt.text()
            
            self.Port =Port
            Storage = self.line_sto.text()
            
            self.Storage =Storage
            
            
            return True
        except Exception as e:
                print(e)
                return False      
            
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
            fn = self.listn.currentItem().text()
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
            sys.exit()
        else:
            sys.exit()    
                
        
        
        
    @pyqtSlot(str)
    def threadEventHandler(self, n):
        print(n)
        self.textv.append(n)
         
    #디렉토리 파일 보여주기       
    def list_show(self):   
        file_list1 = os.listdir(self.Storage)
        self.listn.clear()
        for file in file_list1: 
            if file.endswith(".txt") or file.endswith(".png") or file.endswith(".jpg"):
                self.listn.addItem(file)
            
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
        
        
        
        
        
        
      

        
           
        
           
                
        





