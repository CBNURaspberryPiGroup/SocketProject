import os
import socket




class filelist() :
    def __init__(self,client,storage) :
        self.storage =storage
        self.client = client
        

    def list_f(self):
        file_list1 = os.listdir(self.storage)
        
        
        file_list =[]
        # file_list.append([file for file in file_list1 if file.endswith(".txt")])
        # file_list.append([file for file in file_list1 if file.endswith(".png")])
        # file_list.append([file for file in file_list1 if file.endswith(".jpg")])
        for file in file_list1: 
            if file.endswith(".txt") or file.endswith(".png") or file.endswith(".jpg") or file.endswith(".avi") or file.endswith(".mp4") file.endswith(".mp3"):
                file_list.append(file)

        print (file_list)
        self.client.sendall(str(file_list).encode())
