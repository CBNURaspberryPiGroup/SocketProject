import pyautogui
from time import sleep
#avi converter 실행시킨 상태로 해야함
#exefileopen 한번 들어가서 미리 exe파일있는 폴더로 들어가 놔야함

exefileopen = pyautogui.locateCenterOnScreen('exefileopen.png')
ch1 = pyautogui.locateCenterOnScreen('ch1.png')
ch2 = pyautogui.locateCenterOnScreen('ch2.png')
ch3 = pyautogui.locateCenterOnScreen('ch3.png')
ch4 = pyautogui.locateCenterOnScreen('ch4.png')
start = pyautogui.locateCenterOnScreen('start.png',confidence=0.80)

class Macro():
   
    
    
    def __init__(self):
            super().__init__()
           

            self.exeopen('20201129')  # 매크로시작
           
            self.start(ch1,'1')
            self.start(ch2,'2')
            self.start(ch3,'3')
            self.start(ch4,'4')
            
         

   
    def exeopen(self,filename):              #파일열기
        pyautogui.click(exefileopen)
        sleep(3)  
        pyautogui.typewrite(filename, interval=0.25)
        pyautogui.press('enter')
        sleep(5)
  
        
    def start(self,w,c):
        pyautogui.click(w)
        sleep(2)
        pyautogui.click(start)
        sleep(2)
        pyautogui.press([c,'enter'])
        sleep(25)
        print('25')
        
    
 
    
    
    
    
    
    
   
mc =Macro()
mc.start()    