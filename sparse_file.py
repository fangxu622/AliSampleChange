# -*- coding: utf-8 -*-

import os
import random
import shutil

# def file_name(file_dir):
#     for root, dirs, files in os.walk(file_dir):
#         print(root)  # 当前目录路径
#         print(dirs)  # 当前路径下所有子目录
#         print(files)  # 当前路径下所有非目录子文件
def sparse_file(src_path,target_path,select_c):
    src_path=src_path #"r"+"H:\QdSampleChange"
    target_path=target_path #r"D:\sparse"
    select_count=int(select_c)/2 #随机稀疏参数

    list_1=os.listdir(src_path)

    print "total file count",len(list_1)

    filter_list=[elem for elem in list_1 if "_after" in elem]
    sparse_list=random.sample(filter_list,select_count)
    i=0
    for x in sparse_list:
        i=i+1
        old_path_after=src_path+"/"+x
        old_path_before = old_path_after.replace("_after","_before")
        shutil.copy(old_path_after, target_path)
        shutil.copy(old_path_before, target_path)
        if(i %200==0):
            print "copied number file :"+str(i)+""

    print "successful copy file number "+ str(i*2)

if __name__ == '__main__':
    print "params: src_folder,target_folder,sparse_count"
    import sys
    if(len(sys.argv)<4):
        print "please input params :src_folder,target_folder,sparse_count"
    else:
        sparse_file(sys.argv[1],sys.argv[2],sys.argv[3])
    #for arg in sys.argv:
        #print arg
#print len(filter_list)
