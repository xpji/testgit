# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 17:39:00 2021

@author: 纪
"""

import seaborn as sns
from matplotlib.ticker import AutoMinorLocator, MultipleLocator
import xarray as xr
import netCDF4 as nc
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#read nc file
path='D:\\desktopppp\\sst_olr\\interp_nan\\sst_interp_1982_2012.nc'
ds=xr.open_dataset(path)
path1='D:\\desktopppp\\sst_olr\\interp_nan\\olr_1982_2012.nc'
da=xr.open_dataset(path1)
path2='D:\\desktopppp\\sst_olr\\interp_nan\\hadv_interp_0814.nc'
hadv=xr.open_dataset(path2)
#select range that you need
lat=ds['lat']
lon=np.array(ds['lon'])
lat_range= lat[(lat>-22.5) & (lat<22.5)]
lon_range=lon[(lon>=120)&(lon<=260)]
sst=ds.sel(lat=lat_range)['sst']
olr=da.sel(lat=lat_range)['olr']
hadv=hadv.sel(lat=lat_range)['hadv']
#将数据按照年进行平均处理
#===============筛选0MSE平流强度的sst，olr数据 ==============================


for i in hadv:
     indx=(-25<=hadv)&(hadv<=25)
     sst_31=((np.array(sst))[indx])
     olr_31=((np.array(olr))[indx])

# #select 以0.25°C为一个bins 落入该区间内的数据进行分组,并统计个数
sst_range=np.arange(20,32,0.25)
num=[]
sst_bin=[]
olr_bin=[]
# 做一个循环处理
for i in sst_range:
    
    idx=(sst_31>=i)&(sst_31<=i+0.25) #bool索引，true or false
    sst_bin.append(sst_31[idx])
    olr_bin.append(olr_31[idx])
    ol=olr_31[idx]
    num.append(len(ol))
    
# #对于每一个区间里的olr数据进行求mean std     
olr_mean=[]
sst_mean=[]

olr_std=[]
    
for  j in range(len(olr_bin)):
    
    olr_mean.append(np.mean(olr_bin[j]))
    # olr_std.append((np.std(olr_bin[j])))
for  i in range(len(sst_bin)):
     
    sst_mean.append(np.array(np.mean(sst_bin[i])))
olr_mean=np.array(olr_mean)
olr_bin=np.array(olr_bin)
sst_bin=np.array(sst_bin)
o2=[]

for i in range(len(olr_bin)):
      o2.append(np.array((olr_bin[i]-olr_mean[i])*(olr_bin[i]-olr_mean[i])))
for i in range(len(o2)):
      olr_std.append(sum(o2[i])/len(olr_bin[i]))
     
olr_std=np.array(np.sqrt(olr_std))
sst_bin=np.array(sst_bin)
# #===============================计算 olr随sst的变化率====================
diff=np.gradient(olr_mean)  /0.25 

##===========================================================================
y1=olr_mean+olr_std
y2=olr_mean-olr_std
#=================================plot=================================
x=sst_range
y=olr_mean
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
fig=plt.figure(figsize=(15,6))
ax = fig.add_subplot(1,2,1)

# fig.tight_layout() 
plt.tick_params(labelsize=15)
#散点图
ax.scatter(sst_31,olr_31,s=1)
ax.invert_yaxis()
ax.set_ylim(340,160)
ax.set_xlim(20,31)
ax.plot(x,y,'r',linewidth=3)    #
ax.set_xlabel('SST($°$C)',fontsize=20)
ax.tick_params( axis='x',direction='in',labelsize=20,pad=10)
ax.tick_params(axis='y',direction='in',labelsize=20,pad=10)
ax.set_xticks(np.linspace(20, 32, 7))
ax.set_yticks(np.linspace(160, 340, 10))
ax.set_ylabel('OLR(w/m$^2$)',fontsize=20,color='k')
ax.set_title('0 MSE平流强度下OLR对SST敏感度关系',fontsize=20)
ax.fill_between(x, y1, y2,alpha=0.3,facecolor='r', where=y2 >= y1,  interpolate=True)
ax.fill_between(x, y1, y2, alpha=0.3,facecolor='r',where=y2 <= y1,  interpolate=True)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.tick_params(axis='y',which='major', length=10)
ax.tick_params(axis='x',which='major', length=10)
#=====================dolr/dsst===========================
ax1 = fig.add_subplot(1,2,2)
ax1.plot(sst_range,diff)
ax1.tick_params(axis='y',direction='in',labelsize=20,pad=10)
ax1.tick_params(axis='x',direction='in',labelsize=20,pad=10)
ax1.tick_params(axis='y',which='major', length=10)
ax1.tick_params(axis='x',which='major', length=10)
ax1.set_xlabel('SST($°$C)',fontsize=20)
ax1.set_ylabel('Changing rate(w/m$^2$/°C)',fontsize=20)
ax1.set_title(' $\partial $OLR/$\partial $SST',fontsize=20)
ax1.set_xticks(np.linspace(20, 31, 12))
ax1.set_xlim(20,31)
ax1.set_ylim(10,-15)
ax1.set_yticks(np.linspace(10, -20, 7))
plt.axhline(y=0,linestyle='--',color='grey')
#============================================================

fig.savefig('D:\\desktopppp\\sst_olr\\picture\\'+'0mse.tiff',format='tiff',dpi=150)

d={'0mse':olr_mean}
df=pd.DataFrame(d)  
df.to_csv('D:\\desktopppp\\sst_olr\\'+'0mse.csv') 
d1={'0diff':diff}
df1=pd.DataFrame(d1)  
df1.to_csv('D:\\desktopppp\\sst_olr\\'+'0diff.csv') 