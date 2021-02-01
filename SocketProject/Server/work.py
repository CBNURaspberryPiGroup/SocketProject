import os
class filelist() :
    def __init__(self,client) :
        files = os.listdir()
        curfiles = os.listdir(os.curdir) 

        print(files)
        print('\n')
        print(curfiles)
        print('\n')
        client.sendall(files.encode())
   
    def fileinf(self) :
        if os.path.isfile() :
            print('plain file')

        elif os.path.dir() :
            print('directory')

        else : print('nothing')

        last_acc = os.path.getatime()
        last_modification = os.path.getmtime()
        size = os.path.getsize()
        print(last_acc, last_modification, size)
        print('hi')
