from socket import socket
import msvcrt
import sys

class client_id :
    def Idmodify (self) :
        self.server.recv(1024)
        print("ID를 입력하세요.")
        ID = input("ID를 입력하세요.:")
        ID_list = ID.split()
        if " " in ID : print("공백은 사용할 수 없습니다.")
        elif len(ID_list) >= 8 : print("ID는 8자 이하로 입력하세요")
        elif len(ID_list) <= 3: print("ID는 3자 이상 입력하세요")
        print("ID 처리 완료")
        self.server.sendall(ID)

        
    def pwmodify(prompt = "Password를 입력하세요:"):
        self.server.recv(1024)
        sys.stdout.write(prompt)
        sys.stdout.flush()
        buf = bytearray()
        skip = False
        while True:
            if not msvcrt.kbhit() : continue
            x: bytes = msvcrt.getch()
            if x.startswith(b"\xe0") or x.startswith(b"\x00"):
                skip = True
                continue
            if skip:
                skip = False
                continue
            n = int.from_bytes(x, sys.byteorder)
            if n == 13:
                #Enter
                msvcrt.putch('\n'.encode())
                return buf.decode()
            elif n == 8 :
                if buf:
                    sys.stdout.write("\b \b")
                    sys.stdout.flush()
                    buf.pop()
            elif 32 <= n < 126:
                msvcrt.putch('*'.encode())
                buf.append(n)
        self.server.sendall(Password)

    if __name__ == "__main__":
        print(get_password()) 
        
    def register_id(self) :
        self.server.recv(1024)
        print("등록하고 싶은 ID를 입력하세요.")
        ID = input("ID를 입력하세요.:")
        ID_list = ID.split()
        if " " in ID : print("공백은 사용할 수 없습니다.")
        elif len(ID_list) >= 8 : print("ID는 8자 이하로 입력하세요")
        elif len(ID_list) <= 3: print("ID는 3자 이상 입력하세요")
        print("ID 처리 완료")
        self.server.sendall(ID)

    def register_Pw(self) :
        self.server.recv(1024)
        print("등록하고 싶은 Password를 입력하세요.")
        Password = input("Password를 입력하세요.:")
        Password_list = Password.split()
        if " " in Password : print("공백은 사용할 수 없습니다.")
        elif len(Password_list) >= 6 : print("ID는 6자 이하로 입력하세요")
        elif len(Password_list) <= 4: print("ID는 4자 이상 입력하세요")
        
        while True :
            Password2 = input("Password를 한번 더 입력하세요.:")
            if " " in Password : print("공백은 사용할 수 없습니다.")
            elif len(Password_list) >= 6 : print("ID는 6자 이하로 입력하세요")
            elif len(Password_list) <= 4: print("ID는 4자 이상 입력하세요")

            if Password == Password2 :
                self.server.sendall(Password2) 
                break
            else : print("첫번째 비밀번호와 두번째 비밀번호가 일치하지 않습니다.")