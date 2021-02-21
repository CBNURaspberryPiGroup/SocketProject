import os
file_list1 = os.listdir('./')
for file in file_list1: 
    if file.endswith(".txt") or file.endswith(".png") or file.endswith(".jpg"):
        print(file)