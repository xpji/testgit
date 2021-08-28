# -*- coding: utf-8 -*-
"""
Created on Tue Aug 24 19:49:55 2021

@author: 纪
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

path1='D:\\desktopppp\\olr_mean.csv'
path2='D:\\desktopppp\\diff.csv'
da=pd.read_csv(path1)
ds=pd.read_csv(path2)
#==================读取olr均值、olr随sst变化率
olr=np.array(da['0mse'])#olr均值
diff=np.array(ds['0diff'])#偏导变化率
sst=np.arange(20,32,0.25)

# act=np.trapz(diff)

plt.rcParams['font.sans-serif'] = ['Times new Roman']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
fig=plt.figure(figsize=(10,6))
ax=fig.add_subplot(111)
ax.invert_yaxis()
ax.tick_params( axis='x',direction='in',labelsize=15,pad=10)
ax.tick_params(axis='y',direction='in',labelsize=15,pad=10)
ax.plot(sst,olr,'r',label='OLR')

# # #
ax.plot(sst,act,linewidth=5,label='ACT')
ax.set_xlim(20,31)
ax.set_xticks(np.linspace(20, 31, 12))
ax.set_ylim(270,230)