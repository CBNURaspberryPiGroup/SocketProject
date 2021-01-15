import shutil as sh
import os
import pyautogui
from time import sleep

path = "C:\\Users\\user\\Desktop\\"
fScan = os.scandir(path+"565")
FL = []
for ent in fScan:
    if ".exe" in ent.name : FL.append(ent.name)

#print(FL)
exe2avi = path+"565\\"
wdir = exe2avi+"wdir\\"

for ent in FL:
    sh.copy(exe2avi+ent,wdir+ent)
    print("copy complete")
  
    
    
  
    os.remove(wdir+ent)
    print("remove complete")

    vScan = os.scandir(wdir[:-1])
    for vd in vScan:
        if ".avi" in vd.name :
            dstDir = exe2avi+"CAM%s"%vd.name[-5]
            sh.move(wdir+vd.name,dstDir)
            os.rename(dstDir+"\\"+vd.name,dstDir+"\\"+ent[:-4]+['a','b','c','d'][int(vd.name[-5])-1]+".avi")
        if ".smi" in vd.name :
            dstDir = exe2avi+"smi"
            sh.move(wdir+vd.name,dstDir)
            os.rename(dstDir+"\\"+vd.name,dstDir+"\\"+ent[:-4]+['a','b','c','d'][int(vd.name[-5])-1]+".smi")
        print("--process complete about %s"%vd.name)
    print("process complete about %s"%ent)
    
class Macro():
       
    #aviconverter 켜놔야함 보이게
    
    def __init__(self):
            super().__init__()
           

            self.exeopen(ent)  # 매크로시작
           
            self.start(ch1,'1')     #cam1
            self.start(ch2,'2')     #cam2
            self.start(ch3,'3')     #cam3
            self.start(ch4,'4')     #cam4
            
         

   
    def exeopen(self,filename):              #파일열기
        pyautogui.click(exefileopen)
        sleep(3)  
        pyautogui.typewrite(filename, interval=0.25)
        pyautogui.press('enter')
        sleep(5)
  
        
    def start(self,w,c):    # 비디오 변환하는 부분
        pyautogui.click(w)
        sleep(2)
        pyautogui.click(start)
        sleep(2)
        pyautogui.press([c,'enter'])
        sleep(25)
        print('25')    
#이미지 부분       
exefileopen = pyautogui.locateCenterOnScreen('exefileopen.png')
ch1 = pyautogui.locateCenterOnScreen('ch1.png')
ch2 = pyautogui.locateCenterOnScreen('ch2.png')
ch3 = pyautogui.locateCenterOnScreen('ch3.png')
ch4 = pyautogui.locateCenterOnScreen('ch4.png')
start = pyautogui.locateCenterOnScreen('start.png',confidence=0.80)        