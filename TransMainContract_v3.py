# coding=utf-8

import pandas as pd
import re,os

regexI = '^I[0-9]{4}'
regexi = '^i[0-9]{4}'
regexJ = '^J[0-9]{4}'
regexj = '^j[0-9]{4}'
KeyDateIJ = ['0315','0801','1201']
#list = ['contract','datetime','lp']
list = [0,1,2]
Ifiles = []
Jfiles = []
IMainfiles = []
JMainfiles = []
IMainFile = "I_MainContract.csv"
JMainFile = "J_MainContract.csv"

path = 'data/'
#path = './'
allfiles = os.listdir(path)

### 根据合约名和日期，判断是否为主力合约(焦煤、铁矿、焦炭)
def CheckCodeDate(KeyDateIJ,contract,filedate):
    fileyear = filedate[:4]
    shortyear = fileyear[-2:]
    fileday = filedate[-4:]
    keydate0 = str(int(fileyear)-1)+KeyDateIJ[2]    #上年1201
    keydate0 = fileyear+'0101'          #0101
    keydate1 = fileyear+KeyDateIJ[0]    #今年0315
    keydate2 = fileyear+KeyDateIJ[1]    #今年0801
    keydate3 = fileyear+KeyDateIJ[2]    #今年1201
    keydate4 = str(int(fileyear)+1)+KeyDateIJ[0]    #下面0315
    if (keydate0 <= filedate) and (filedate <= keydate1) and ((shortyear+'05') in contract): return True   #1201-0315,今年05
    elif (keydate1 <= filedate) and (filedate <= keydate2) and ((shortyear+'09') in contract): return True   #0315-0801,今年09
    elif (keydate2 <= filedate) and (filedate <= keydate3) and ((str(int(shortyear)+1)+'01') in contract): return True   #0801-1201,下年01
    elif (keydate3 <= filedate) and (filedate <= keydate4) and ((str(int(shortyear)+1)+'05') in contract): return True   #1201-0315,下年05

### 根据合约读取切换日的部分数据
def ReadPart(file,codeend,fileday):
    codedaycode = {'0315':['05','09'],'0801':['09','01'],'1201':['01','05']}
    # 查找切换日期的行index
    tempdata = pd.read_csv(file, encoding='gbk', dtype=str, usecols=list)
    tempdata.rename(columns={'dt':'datetime'},inplace = True)
    for index, row in tempdata.iterrows():
        if (fileday[:2]+'-'+fileday[-2:]) in row.datetime:
            keyline = index
            break
    # 前面的合约，读取切换之前的数据
    if codeend == codedaycode[fileday][0]:
        data = pd.read_csv(file,encoding='gbk',dtype=str,usecols=list,nrows=keyline)
    # 后面的合约，跳过切换之前的数据，但要保留标题行
    elif codeend == codedaycode[fileday][1]:
        templine = []
        for i in range(1,keyline+1):
            templine.append(i)
        data = pd.read_csv(file,encoding='gbk',dtype=str,usecols=list,skiprows=tuple(templine))
    return data

##################### Main ########################
### 根据文件名划分焦炭和铁矿
for item in allfiles:
    if re.match(regexI,item) or re.match(regexi,item): Ifiles.append(item)
    elif re.match(regexJ,item) or re.match(regexj,item): Jfiles.append(item)
### 根据文件名中的日期及合约名，判断是否为主力合约
for item in Ifiles:     #铁矿
    contract = item[0:5]
    filedate = item.rstrip('.csv')[-8:]
    if CheckCodeDate(KeyDateIJ,contract,filedate):
        IMainfiles.append(item)
for item in Jfiles:     #焦煤
    contract = item[0:5]
    filedate = item.rstrip('.csv')[-8:]
    if CheckCodeDate(KeyDateIJ,contract,filedate):
        JMainfiles.append(item)
### 读取并合并主力合约数据
for item in IMainfiles:
    print("Read file: %s" % item)
    file = path+item
    codeend = item.split('_')[0][-2:]
    fileday = item.rstrip('.csv')[-4:]
    if fileday in KeyDateIJ: date = ReadPart(file,codeend,fileday)
    else: data = pd.read_csv(file,encoding='gbk',dtype=str,usecols=list)
    if os.path.exists(IMainFile):
        data.to_csv(IMainFile,index=0,mode='a',header=0)
    else:
        data.to_csv(IMainFile, index=0,mode='w')

for item in JMainfiles:
    print("Read file: %s" % item)
    file = path+item
    codeend = item.split('_')[0][-2:]
    fileday = item.rstrip('.csv')[-4:]
    if fileday in KeyDateIJ: date = ReadPart(file,codeend,fileday)
    else: data = pd.read_csv(file,encoding='gbk',dtype=str,usecols=list)
    if os.path.exists(JMainFile):
        data.to_csv(JMainFile, index=0, mode='a', header=0)
    else:
        data.to_csv(JMainFile, index=0, mode='w')

