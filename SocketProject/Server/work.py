import os
import socket




class filelist() :
    def __init__(self,client,storage) :
        self.storage =storage
        self.client = client
        

    def list_f(self):
        file_list1 = os.listdir(self.storage)
        
        
        file_list =[]
        file_list.append([file for file in file_list1 if file.endswith(".txt")])
        file_list.append([file for file in file_list1 if file.endswith(".png")])

        print (file_list)
        self.client.sendall(file_list.encode())
