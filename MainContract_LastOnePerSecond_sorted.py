# coding=utf-8
import os
import pandas as pd
from datetime import datetime

filename = 'data/I_MainContract.csv'
filename = 'I_MainContract.csv'
tempfilename = filename.split('.')[0]+"_temp.csv"
sortedfilename = filename.split('.')[0]+'_Sorted.csv'

print("开始反转文件")
df = pd.read_csv(filename,encoding='gbk', dtype=str)
#df = df[:1000]
df2 = df.sort_index(ascending=False)    #数据倒序，变为查找相同分钟的第一个数据
tempfile = open(tempfilename,mode='w')
print('contract','datetime','lp',sep=',',file=tempfile)

print("开始筛选分钟数据")
existdts = []   #存放已有日期时间
df3 = pd.DataFrame
for index,row in df2.iterrows():
    recdatetime = row.datetime
    if '.' in recdatetime:
        recdt = recdatetime.split('.')[0]
    else:
        recdt = recdatetime
    if not (recdt in existdts):
        existdts.append(recdt)
        print(recdt)
        print(row.contract, recdt, row.lp, sep=',',file=tempfile)
        #tempfile.flush()
tempfile.close()    #将倒序且含唯一分钟时间的数据保存为临时文件

print("开始排序")
data = pd.read_csv(tempfilename)
#for index,row in data.iterrows():
#    timedate = datetime.strptime(row.datetime, '%Y-%m-%d %H:%M:%S')
#    data.iloc[index, 1] = timedate
data2 = data.sort_values(by='datetime')
data2.to_csv(sortedfilename,index=0)
#if os.path.exists(tempfilename): os.remove(tempfilename)
