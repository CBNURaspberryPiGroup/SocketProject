import socket
import Commmand
import work
import Send
import Logging as Log
from os.path import exists
import time


Host = '1.246.117.24'
Port = 9966

storage = "./"

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

if not exists("log.log") :
    Log.startlog()

server_socket.bind((Host,Port))
def sever():
        print("listening...")
        server_socket.listen()
        print("listened")
        client, addr = server_socket.accept()
        print('Connected by '+str(addr))
        Log.log(1,"Connected by "+str(addr))
        a = 0
        while True :
            a += 1
            Com = Commmand.Command(client,storage)
            if a == 1 : 
                Com.split2()
            wok=work.filelist(client,storage)
        
            wok.list_f()
            print('명령어 대기상태')
            Com.split()
           
    
while True:            
    try:
        sever()
        
        
    except Exception as e:
        
        print(e)
        pass
        
    
