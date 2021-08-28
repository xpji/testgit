# -*- coding: utf-8 -*-
"""
Created on Wed Aug 11 10:49:12 2021

@author: 纪
"""



import cartopy.crs as ccrs
import pandas as pd
import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt


path1='D:\\desktopppp\\olr_mean.csv'
path2='D:\\desktopppp\\diff.csv'
da=pd.read_csv(path1)
ds=pd.read_csv(path2)
#==================
dif0=ds['0diff']
x=np.arange(20,32,0.25)
#=======================最小二乘法==========================================





plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
fig=plt.figure(figsize=(10,6))
ax=fig.add_subplot(111)
ax.invert_yaxis()
ax.tick_params( axis='x',direction='in',labelsize=15,pad=15)
ax.tick_params(axis='y',direction='in',labelsize=15,pad=15)
ax.plot(x,dif0,'b',label='$\partial $OLR/$\partial $SST')
ax.set_xlim(20,31)
ax.set_xticks(np.linspace(20, 31, 12))
ax.set_ylim(10,-10)#末尾不显示210，280
ax.set_yticks(np.linspace(10, -20, 6))
ax.set_title(' $\partial $OLR/$\partial $SST and EOT',fontsize=20)
ax.set_ylabel('Changing rate(w/m$^2$/°C)',fontsize=20)
ax.set_xlabel('SST($°$C)',fontsize=20)
plt.axhline(y=0,linestyle='-',color='orange',xmin=0,xmax=0.472,linewidth=3)
plt.axhline(y=0,linestyle='-',color='orange',xmin=0.87,xmax=1,linewidth=3)
plt.axvline(x=29.5,linestyle='--',color='grey')
plt.axvline(x=25.25,linestyle='--',color='grey')
# plt.axvline(x=28.75,linestyle='--',color='deepskyblue')
ax.plot(x[21:39],dif0[21:39],'orange',linewidth=5,alpha=0.5,label='EOT')
ax.legend()
fig.savefig('D:\\desktopppp\\sst_olr\\picture\\'+'OLR_SST and EOT.tiff',format='tiff',dpi=150)





















