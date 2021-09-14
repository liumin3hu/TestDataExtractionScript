# -*- coding: utf-8 -*-
#!/usr/bin/python 
import os
import re
import csv
import string

result = []
keysummary='.summary'
def get_subdir(cwd):
    global dir_flag
    get_dir = os.listdir(cwd)  
    for i in get_dir:          
        sub_dir = os.path.join(cwd,i)  
        if os.path.isdir(sub_dir):  
            get_subdir(sub_dir)
        else:
            matchObj = re.search( keysummary, i)
            if matchObj !=None:
                readSummaryFile(sub_dir)
                writeToCsv(cwd)
                result.append(i)

def readSummaryFile(file_name):
    flag=0
    cnt=0
    keyList=['prefix-cql-tabular.bind','prefix-cql-tabular.cycles.servicetime','prefix-cql-tabular.execute','prefix-cql-tabular.phases.servicetime','prefix-cql-tabular.read_input','prefix-cql-tabular.strides.servicetime']
    with open(file_name) as file_obj:
        for content in file_obj:
            if flag==0:
                for item in keyList:
                    matchObj = re.search( item, content)
                    if matchObj != None:
                        flag=1
            if flag==1:
                if cnt==0:
                    cnt+=1
                elif cnt==15:
                    flag=0
                    cnt=0
                else:
                    getContentData(content)
                    cnt+=1

  
dataList=[]
def getContentData(content):
    keychar='='
    endkeychar='m'
    global dataList
    columonList=['min =','max =','mean =','stddev','median','95%']
    if content != ' ':
        for item in columonList:
            matchObj = re.search( item, content)
            if matchObj != None:
                contentItem=content[content.index(keychar)+2:]
                contentItem=re.sub("[^0-9.]", "",contentItem)
                contentItem=contentItem.replace('\n',' ')
                dataList.append(contentItem)
    


def writeToCsv(sub_dir):
    global dataList
    global filename
    global logsFlowder
    stringFlag='.'
    filenamecsv=getFileName(sub_dir)+'.csv'
    path=sub_dir+'/'+filenamecsv
    with open(path,"a",newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(dataList)  
        csvfile.close()
        dataList=[]
        
def getFileName(sub_dir):
    keyChar='/'
    fileType='.csv'
    cnt=0
    keyCharEndPosition=0
    if sub_dir != '':
        for item in sub_dir:
            if item==keyChar:
                keyCharEndPosition=0
                cnt += 1
                keyCharEndPosition += cnt
            else:
                cnt += 1
    filename=sub_dir[keyCharEndPosition:]
    return filename
            



if __name__ == "__main__": 
    get_subdir(r'/home/chx/work/partofcassandra')
    