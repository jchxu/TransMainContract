# coding=utf-8

import pandas as pd
from datetime import datetime

filename = 'I_MainContract-test.csv'
df = pd.read_csv(filename)
#filedata = pd.read_csv(filename,sep=',',encoding='gbk',dtype='datetime64[ns]',usecols=['TDATETIME'])
filedata = pd.read_csv(filename,sep=',',encoding='gbk',dtype='str',usecols=['TDATETIME'])

print(filedata)
#print(df.iloc[1,2])
#print(df[:5])
for index,row in df.iterrows():
    timedate = datetime.strptime(row.TDATETIME.split('.')[0], '%Y-%m-%d %H:%M:%S')
    df.iloc[index, 1] = timedate

df2 = df.sort_values(by='TDATETIME')
newfilename = filename.split('.')[0] + '_Sorted.csv'
df2.to_csv(newfilename,index=0)