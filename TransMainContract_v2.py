# coding=utf-8

import pandas as pd
import re

yearlist = [2014,2015,2016,2017,2018]
prefix = "MFL1_TRDMIN01_"
filestyle = ".csv"
regexRB = '^RB[0-9]{4}'
regexI = '^I[0-9]{4}'
keyRB = ['03-15','08-20','12-01']
keyI = ['03-15','08-01','12-01']
list = ['CONTRACTID', 'TDATETIME', 'OPENPX', 'HIGHPX', 'LOWPX', 'LASTPX', 'MINQTY', 'TURNOVER', 'OPENINTS', 'CHGMIN', 'CHGPCTMIN']
RBresfile = open(file='RB_MainContract.csv',mode='w')
Iresfile = open(file='I_MainContract.csv',mode='w')

def checkRBrecdate(recdate,recyear,keyRB):
    keyRBdate0 = str(int(recyear)-1) + '-' + keyRB[2]
    keyRBdate1 = recyear + '-' + keyRB[0]
    keyRBdate2 = recyear + '-' + keyRB[1]
    keyRBdate3 = recyear + '-' + keyRB[2]
    keyRBdate4 = str(int(recyear)+1) + '-' + keyRB[0]
    if keyRBdate0 <= recdate and recdate < keyRBdate1:
        return ('RB'+recyear[2:4]+'05')
    elif keyRBdate1 <= recdate and recdate < keyRBdate2:
        return ('RB'+recyear[2:4]+'10')
    elif keyRBdate2 <= recdate and recdate < keyRBdate3:
        return ('RB'+str(int(recyear[2:4])+1)+'01')
    elif keyRBdate3 <= recdate and recdate < keyRBdate4:
        return ('RB'+str(int(recyear[2:4])+1)+'05')
def checkIrecdate(recdate,recyear,keyI):
    keyIdate0 = str(int(recyear)-1) + '-' + keyI[2]
    keyIdate1 = recyear + '-' + keyI[0]
    keyIdate2 = recyear + '-' + keyI[1]
    keyIdate3 = recyear + '-' + keyI[2]
    keyIdate4 = str(int(recyear)+1) + '-' + keyI[0]
    if keyIdate0 <= recdate and recdate < keyIdate1:
        return ('I'+recyear[2:4]+'05')
    elif keyIdate1 <= recdate and recdate < keyIdate2:
        return ('I'+recyear[2:4]+'09')
    elif keyIdate2 <= recdate and recdate < keyIdate3:
        return ('I'+str(int(recyear[2:4])+1)+'01')
    elif keyIdate3 <= recdate and recdate < keyIdate4:
        return ('I'+str(int(recyear[2:4])+1)+'05')
print('CONTRACTID', 'TDATETIME', 'OPENPX', 'HIGHPX', 'LOWPX', 'LASTPX', 'MINQTY', 'TURNOVER', 'OPENINTS', 'CHGMIN', 'CHGPCTMIN',sep=',',file=RBresfile)
print('CONTRACTID', 'TDATETIME', 'OPENPX', 'HIGHPX', 'LOWPX', 'LASTPX', 'MINQTY', 'TURNOVER', 'OPENINTS', 'CHGMIN', 'CHGPCTMIN',sep=',',file=Iresfile)

# 根据年份和月份获取csv文件名
for i in range(2014,2019):
    for j in range(1,13):
        RBRec = []
        IRec = []
        dt = str(i) + (format('%02d') % j)    #yyyymm
        if dt <= '201602':  #指定读取截止时间
            filename = prefix + dt + filestyle
            print('Reading %s' % filename)
            # 读取csv文件中指定列的数据
            filedata = pd.read_csv(filename,sep=',',encoding='gbk',dtype=str,usecols=list)#,nrows=10000)
            for index,row in filedata.iterrows():
                # 根据CONTRACTID是否以指定字母开头，判断属于什么品种，并加入相应list中
                if re.match(regexRB,row.CONTRACTID):
                    RBRec.append(row)
                elif re.match(regexI,row.CONTRACTID):
                    IRec.append(row)
            del filename
            print('Total %d RB**** records' % len(RBRec))
            print('Total %d I**** records' % len(IRec))
        # 根据时间节点筛选RB主力合约 ###
            for item in RBRec:
                recdate = item.TDATETIME.split()[0]
                recyear = item.TDATETIME[0:4]
                maincontract = checkRBrecdate(recdate, recyear, keyRB)
                if item.CONTRACTID == maincontract:
                    print(item.CONTRACTID, item.TDATETIME, item.OPENPX, item.HIGHPX, item.LOWPX, item.LASTPX, item.MINQTY, item.TURNOVER, item.OPENINTS, item.CHGMIN, item.CHGPCTMIN,sep=',',file=RBresfile)
        # 根据时间节点筛选I主力合约 ###
            for item in IRec:
                recdate = item.TDATETIME.split()[0]
                recyear = item.TDATETIME[0:4]
                maincontract = checkIrecdate(recdate, recyear, keyI)
                if item.CONTRACTID == maincontract:
                    print(item.CONTRACTID, item.TDATETIME, item.OPENPX, item.HIGHPX, item.LOWPX, item.LASTPX, item.MINQTY, item.TURNOVER, item.OPENINTS, item.CHGMIN, item.CHGPCTMIN,sep=',',file=Iresfile)
RBresfile.close()
Iresfile.close()