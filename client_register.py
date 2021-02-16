from socket import socket
import msvcrt
import sys


class client_id :
    def __init__ (self, client) :
        self.client = client

    def Id_login (self) :
        id = self.client.recv(1024)
        Deid = id.decode()
        print("ID를 입력하세요.")
        
        while True :
            ID = input(Deid)
            ID_list = ID.split()
            if " " in ID : print("공백은 사용할 수 없습니다.")
                True
            elif len(ID_list) >= 8 : print("ID는 8자 이하로 입력하세요")
                True
            elif len(ID_list) <= 3: print("ID는 3자 이상 입력하세요")
                True
            else : False
        print("ID 처리 완료")
        self.client.sendall(ID.encode)

        
    def pw_login(self) :
        pw = self.client.recv(1024)
        depw = pw.decode()
        print("pw를 입력하세요.")
            
        while True :
            pw = input(depw)
            pw_list = pw.split()
                if " " in  : print("공백은 사용할 수 없습니다.")
                    True
                elif len(pw_list) >= 8 : print("pw는 8자 이하로 입력하세요")
                    True
                elif len(pw_list) <= 3: print("pw는 3자 이상 입력하세요")
                    True
                else : False
            print("pw 처리 완료")
            self.client.sendall(pw.encode())
        
    def register_id(self, client) :
        id = self.client.recv(1024)
        deid = id.decode()
        print("등록하고 싶은 ID를 입력하세요.")
        while True :
            ID = input(Deid)
            ID_list = ID.split()
            if " " in ID : print("공백은 사용할 수 없습니다.")
                True
            elif len(ID_list) >= 8 : print("ID는 8자 이하로 입력하세요")
                True
            elif len(ID_list) <= 3: print("ID는 3자 이상 입력하세요")
                True
            else : False
        print("ID 처리 완료")
        self.client.sendall(ID.encode)

    def register_Pw(self, client) :
        pw = self.client.recv(1024)
        depw = pw.decode()
        print("등록하고 싶은 Password를 입력하세요.")
        while True :
            pw = input(depw)
            pw_list = pw.split()
                if " " in  : print("공백은 사용할 수 없습니다.")
                    True
                elif len(pw_list) >= 8 : print("pw는 8자 이하로 입력하세요")
                    True
                elif len(pw_list) <= 3: print("pw는 3자 이상 입력하세요")
                    True
                else : False
        pw = self.client.recv(1024)
        depw2 = pw.decode()
        while True :
            depw == input(depw2)
            pw_list = pw.split()
            if " " in depw2 : print("공백은 사용할 수 없습니다.")
            elif len(Pw_list) >= 6 : print("ID는 6자 이하로 입력하세요")
            elif len(Pw_list) <= 4: print("ID는 4자 이상 입력하세요")

            if depw == depw2 :
                self.client.sendall(depw2) 
                break
            else : print("첫번째 비밀번호와 두번째 비밀번호가 일치하지 않습니다.")