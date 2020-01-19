# 文件处理
import os

path1 = '/home/kevenano/Code/python'
for folderName, subfolders, filenames in os.walk(path1):
    print('The current folder is '+folderName)
    for subfolder in subfolders:
        print('SUBFOLDER OF '+folderName+': '+subfolder)
    for filename in filenames:
        print('FILE INSIDE '+folderName+': '+filename)
    print(' ')
