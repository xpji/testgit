4# -*- coding: utf-8 -*-
"""
Created on Wed Aug 11 15:54:52 2021

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
#=======================最小二乘法计算EOT系数=============================
x1=sst[21:36]#25.25-28.75
x2=sst[35:39]#28.75-29.5
A = np.vstack([x1, np.ones(len(x1))]).T
a, b = np.linalg.lstsq(A, diff[21:36], rcond=None)[0]
A2 = np.vstack([x2, np.ones(len(x2))]).T
a2, b2 = np.linalg.lstsq(A2, diff[35:39], rcond=None)[0]
#=======================梯形积分===========================================
act1=[]
i=0.25
while i <3.75:
    idx=(sst>=25.25)&(sst<=25.25+i)
    # print(25.25+i)
    x=sst[idx]
    y=diff[idx]
    act1.append(np.trapz(x*a+b,x)+olr[21])
    i=i+0.25
act2=[]
j=0.25
while j <1:
    indx=(sst>=28.75)&(sst<=28.75+j)
    # print([j+28.75])
    xx=sst[indx]
    yy=diff[indx]
    act2.append(np.trapz(xx*a2+b2,xx)+act1[-1])
    j=j+0.25
act0=[]
act3=[]
for k in sst:
    if k<=25.25:
        # print([k])
        act0.append(k+0.25-k+olr[21])
    elif k>29.5:
        # print([k])
        act3.append(k+0.25-k+act2[-1])
act=act0+act1+act2+act3
#==============================画图=======================================
plt.rcParams['font.sans-serif'] = ['Times new Roman']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
fig=plt.figure(figsize=(10,8))
ax=fig.add_subplot(111)
ax.invert_yaxis()
ax.tick_params( axis='x',direction='in',labelsize=15,pad=10)
ax.tick_params(axis='y',direction='in',labelsize=15,pad=10)
#plot
ax.plot(sst,olr,'orange',label='OLR')
ax.plot(sst,act,'lightblue',linewidth=3,label='ACT')
# # #

ax.set_xlim(20,31)
ax.set_xticks(np.linspace(20, 31, 12))
ax.set_ylim(270,230)
ax.set_yticks(np.linspace(270, 230,9))
ax.set_title(' OLR and ACT',fontsize=20)
ax.set_ylabel('OLR,ACT(w/m$^2$/°C)',fontsize=20)
ax.set_xlabel('SST($°$C)',fontsize=20)
ax.legend()
plt.axhline(y=act[0],linestyle='--',color='grey',xmin=0,xmax=0.476)
plt.axhline(y=act[-1],linestyle='--',color='grey',xmin=0,xmax=0.86)
# plt.axhline(y=ac[35],linestyle='--',color='deepskyblue',xmin=0.,xmax=0.8,linewidth=2)
# plt.axhline(y=ac[0],linestyle='--',color='deepskyblue',xmin=0,xmax=0.48,linewidth=2)
# plt.axvline(x=29.5,linestyle='--',color='deepskyblue',ymin=0,ymax=0.84)
plt.axvline(x=29.5,linestyle='--',color='grey',ymin=0,ymax=0.83)
plt.axvline(x=25.25,linestyle='--',color='grey',ymin=0,ymax=0.116)


# ax1=fig.add_subplot(122)
# ax1.plot(sst,diff)
# ax1.set_xlim(20,31)
# ax1.set_xticks(np.linspace(20, 31, 12))
# ax1.set_ylim(10,-10)#末尾不显示210，280
# ax1.set_yticks(np.linspace(10, -20, 6))
# plt.axvline(x=28.75,linestyle='--',color='deepskyblue',ymin=0,ymax=0.9)
# plt.axvline(x=25.25,linestyle='--',color='deepskyblue',ymin=0,ymax=0.35)
# plt.axvline(x=29.5,linestyle='--',color='deepskyblue',ymin=0,ymax=0.35)
# plt.axhline(y=0,linestyle='--',color='grey',xmin=0,xmax=1)
# fig.savefig('D:\\desktopppp\\sst_olr\\picture\\'+'ACT and OLR.tiff',format='tiff',dpi=150)





















