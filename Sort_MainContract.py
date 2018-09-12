# coding=utf-8

import pandas as pd

filename = 'J_MainContract.csv'
df = pd.read_csv(filename)
df2 = df.sort_values(by='TDATETIME')
newfilename = filename.split('.')[0] + '_Sorted.csv'
df2.to_csv(newfilename,index=0)