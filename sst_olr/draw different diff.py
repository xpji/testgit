# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 22:33:29 2021

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

# olr0=da['0mse_olr_mean']
# y1=olr0+np.sqrt(np.std(olr0))
# y2=olr0-np.sqrt(np.std(olr0))

# olr50=da['50mse_olr_mean']
# y11=olr50+np.sqrt(np.std(olr50))
# y22=olr50-np.sqrt(np.std(olr50))

# olr100=da['100mse_olr_mean']
# y3=olr100+np.sqrt(np.std(olr100))
# y4=olr100-np.sqrt(np.std(olr100))

# olr05=da['-50mse_olr_mean']
# y33=olr05+np.sqrt(np.std(olr05))
# y44=olr05-np.sqrt(np.std(olr05))

# olr001=da['-100mse_olr_mean']
# y5=olr001+np.sqrt(np.std(olr001))
# y6=olr001-np.sqrt(np.std(olr001))


#==================
dif0=ds['0diff']
dif50=ds['50diff']
dif100=ds['100diff']
dif05=ds['-50diff']
dif001=ds['-100diff']

x=np.arange(20,32,0.25)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
fig=plt.figure(figsize=(10,6))
ax=fig.add_subplot(111)
ax.invert_yaxis()
ax.tick_params( axis='x',direction='in',labelsize=15,pad=10)
ax.tick_params(axis='y',direction='in',labelsize=15,pad=10)
ax.plot(x,dif0,'r',label='0 MSE平流强度$\partial $OLR/$\partial $SST')


# ax.plot(x,dif50,'aqua',label='50 MSE平流强度$\partial $OLR/$\partial $SST')


# ax.plot(x,dif100,'orange',label='100 MSE平流强度$\partial $OLR/$\partial $SST')


# ax.plot(x,dif05,'lightgreen',label='-50 MSE平流强度$\partial $OLR/$\partial $SST')


# ax.plot(x,dif001,'k',label='-100 MSE平流强度$\partial $OLR/$\partial $SST')
\
ax.set_xlim(20,30)
ax.set_xticks(np.linspace(20, 31, 12))
# ax.set_ylim(11,-15)#末尾不显示210，280
ax.set_ylim(20,-20)
ax.legend()
ax.set_title(' $\partial $OLR/$\partial $SST',fontsize=20)
ax.set_ylabel('Changing rate(w/m$^2$/°C)',fontsize=20)
ax.set_xlabel('SST($°$C)',fontsize=20)
plt.axhline(y=0,linestyle='--',color='deepskyblue')
# plt.axvline(x=25.25,ymin=0,ymax=0.5,linestyle='--',color='deepskyblue')
fig.savefig('D:\\desktopppp\\sst_olr\\picture\\'+' 0 MSE平流强度下OLR随SST变化率.tiff',format='tiff',dpi=150)