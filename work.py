from socket import *
import os
from os.path import exists
import sys

serverSock = socket(AF_INET, SOCK_STREAM)
serverSock.bind(('', 9966))
serverSock.listen(1)

##
folder=os.getcwd()
print("current directory :" %s) %folder

for filename in os.listdir(folder):
	ext=filename.split('.')[-1]
	if ext == 'exe':
		print(filename)


connectionSock, addr = serverSock.accept()

print(str(addr),'에서 접속했습니다')
path = "./"
file_list = os.listdir(path)
file_list_txt = [file for file in file_list if file.endswith(".txt")]
date =('file_list:{}'.format(file_list_txt))
connectionSock.sendall(date.encode())
filename = connectionSock.recv(1024) #클라이언트한테 파일이름(이진 바이트 스트림 형태)을 전달 받는다
print('받은 데이터 : ', filename.decode('utf-8')) #파일 이름을 일반 문자열로 변환한다
data_transferred = 0

if not exists(filename):
    data=connectionSock.recv(1024)

    nowdir = os.getcwd()
    with open(nowdir+"\\"+filename, 'wb') as f: #현재dir에 filename으로 파일을 받는다
        
        try:
            while data: #데이터가 있을 때까지
                f.write(data) #1024바이트 쓴다
                data_transferred += len(data)
                data = clientSock.recv(1024) #1024바이트를 받아 온다
        except Exception as ex:
            print(ex)
    print('파일 %s 받기 완료. 전송량 %d' %(filename, data_transferred))
    

print("파일 %s 전송 시작" %filename)
with open(filename, 'rb') as f:
    try:
        data = f.read(1024) #1024바이트 읽는다
        while data: #데이터가 없을 때까지
            data_transferred += connectionSock.send(data) #1024바이트 보내고 크기 저장
            data = f.read(1024) #1024바이트 읽음
    except Exception as ex:
        print(ex)
print("전송완료 %s, 전송량 %d" %(filename, data_transferred))
serverSock.close()