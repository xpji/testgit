# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 21:46:25 2021

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

olr0=da['0mse']
y1=olr0+np.sqrt(np.std(olr0))
y2=olr0-np.sqrt(np.std(olr0))

olr50=da['50mse']
y11=olr50+np.sqrt(np.std(olr50))
y22=olr50-np.sqrt(np.std(olr50))

olr100=da['100mse']
y3=olr100+np.sqrt(np.std(olr100))
y4=olr100-np.sqrt(np.std(olr100))

olr05=da['-50mse']
y33=olr05+np.sqrt(np.std(olr05))
y44=olr05-np.sqrt(np.std(olr05))

olr001=da['-100mse']
y5=olr001+np.sqrt(np.std(olr001))
y6=olr001-np.sqrt(np.std(olr001))


#==================
dif0=ds['0diff']
dif50=ds['50diff']
dif100=ds['100diff']
dif05=ds['-50diff']
dif001=ds['-100diff']

x=np.arange(20,32.25,0.25)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
fig=plt.figure(figsize=(10,6))
ax=fig.add_subplot(111)
ax.invert_yaxis()
ax.tick_params( axis='x',direction='in',labelsize=15)
ax.tick_params(axis='y',direction='in',labelsize=15)
ax.plot(x,olr0,'r',label='0 MSE平流强度OLR均值线')
ax.fill_between(x, y1, y2,alpha=0.3,facecolor='lightcoral', where=y2 >= y1,  interpolate=True)
ax.fill_between(x, y1, y2, alpha=0.3,facecolor='lightcoral',where=y2 <= y1,  interpolate=True)

ax.plot(x,olr50,'lightskyblue',label='50 MSE平流强度OLR均值线')
ax.fill_between(x, y11, y22,alpha=0.3,facecolor='lightskyblue', where=y22 >= y11,  interpolate=True)
ax.fill_between(x, y11, y22, alpha=0.3,facecolor='lightskyblue',where=y22 <= y11,  interpolate=True)

ax.plot(x,olr100,'yellow',label='100 MSE平流强度OLR均值线')
ax.fill_between(x, y3, y4,alpha=0.15,facecolor='yellow', where=y4 >= y3,  interpolate=True)
ax.fill_between(x, y3, y4, alpha=0.15,facecolor='yellow',where=y4 <= y3,  interpolate=True)

ax.plot(x,olr05,'lightgreen',label='-50 MSE平流强度OLR均值线')
ax.fill_between(x, y33, y44,alpha=0.3,facecolor='lightgreen', where=y44 >= y33,  interpolate=True)
ax.fill_between(x, y33, y44, alpha=0.3,facecolor='lightgreen',where=y44 <= y33,  interpolate=True)

ax.plot(x,olr001,'k',label='-100 MSE平流强度OLR均值线')
ax.fill_between(x, y5, y6,alpha=0.3,facecolor='grey', where=y6 >= y5,  interpolate=True)
ax.fill_between(x, y5, y6, alpha=0.3,facecolor='grey',where=y6 <= y5,  interpolate=True)
ax.set_xlim(20,31)
ax.set_xticks(np.linspace(20, 31, 12))
ax.set_ylim(285,215)#末尾不显示210，280
ax.legend()
ax.set_title('各MSE平流强度下OLR对SST的敏感度关系')
ax.set_ylabel('OLR(w/m$^2$)',fontsize=20,color='k')
ax.set_xlabel('SST($°$C)',fontsize=20)


fig.savefig('D:\\desktopppp\\sst_olr\\picture\\'+'各MSE平流强度下OLR对SST的敏感度关系.tiff',format='tiff',dpi=150)