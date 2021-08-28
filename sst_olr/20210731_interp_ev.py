# -*- coding: utf-8 -*-
"""
Created on Sat Jul 31 18:32:49 2021

@author: 纪
"""
import seaborn as sns
from matplotlib.ticker import AutoMinorLocator, MultipleLocator
from scipy.optimize import curve_fit
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
from scipy.optimize import leastsq
from itertools import groupby
from scipy import signal
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
#select range that you need
lat=ds['lat']
lat_range= lat[(lat>-22.5) & (lat<22.5)]
# lon_range=lon[(lon)]
sst=ds.sel(lat=lat_range)
olr=da.sel(lat=lat_range)
#将数据按照年进行平均处理
# olr_summary = olr.groupby('time.day').mean('time', skipna=True)
# summary1=summary.olr.mean(dim='year')
# sst_summary = sst.groupby('time.day').mean('time', skipna=True)
#select the first year_mean data 既1982年的年平均数据
sst_1982=np.array(sst.sst)
olr_1982=np.array(olr.olr)
#select 以0.25°C为一个bins 落入该区间内的数据进行分组,并统计个数
sst_range=np.arange(20,32.25,0.25)
num=[]
sst_bin=[]
olr_bin=[]
# 做一个循环处理
for i in sst_range:
    
    idx=(sst_1982>=i)&(sst_1982<=i+0.25) #bool索引，true or false
    sst_bin.append(sst_1982[idx])
    olr_bin.append(olr_1982[idx])
    ol=olr_1982[idx]
    num.append(len(ol))
    
#打开分好组的数据发现大部分分布在15°C-30°C，所以选择该范围的数据进行下一步处理
# sst_bin=np.array(sst_bins[20:60]) 
# olr_bin=np.array(olr_bins[20:60] )
# num=num[20:60] 
#对于每一个区间里的olr数据进行求mean std     
olr_mean=[]
sst_mean=[]
olr_std=[]
sst_std=[]

    
for  j in range(len(olr_bin)):
    
    olr_mean.append(np.mean(olr_bin[j]))
    
    olr_std.append(np.std(np.array(olr_bin[j])))
    
for  i in range(len(sst_bin)):
    sst_mean.append(np.array(np.mean(sst_bin[i])))
    sst_std.append(np.std(sst_bin[i]))
olr_mean=np.array(olr_mean)
sst_mean=np.array(sst_mean)
sst_bin=np.array(sst_bin)
#===============================计算 olr随sst的变化率============================
bins=0.25
change_rate=(olr_mean*(sst_range+bins)-olr_mean*(sst_range-bins))/2*bins
change_rate=np.array(change_rate)
c_rate_mean=[]
for k  in range(len(change_rate)):
    c_rate_mean.append(np.nanmean(change_rate[k]))
num10=np.log10(num)   
#draw scatter mean_plot  
x=sst_mean
y=olr_mean
z=sst_range
#========================nihe
olr_std=np.array(olr_std)
zz=olr_std-2*olr_std

#

fig=plt.figure(figsize=(26,12))
ax = fig.add_subplot(1,2,1)
ax3 = fig.add_subplot(1,2,2)
# fig.tight_layout() 
plt.tick_params(labelsize=15)
# ax=fig.add_subplot(2,1,1)
ax.scatter(sst_1982,olr_1982,s=1,color='grey')
ax.invert_yaxis()
ax.set_ylim(320,160)
ax.set_xlim(20,32)
# ax.grid(color='w')
x_grid=ax.get_xgridlines()
x_grid[3].set_color('k')  
ax.plot(z,y,'r')    #
ax.set_xlabel('SST(°C)',fontsize=15)
ax.spines['left'].set_color ('r')#设置轴的颜色
ax.tick_params( axis='y',direction='out', colors='red',
              labelcolor='r',   labelsize=15)#设置y轴颜色，外凸间隔，字体大小
ax.tick_params( axis='x',direction='out',
            )
ax.tick_params(axis='y',colors='r')
ax.set_xticks(np.linspace(20, 32, 7))
ax.set_yticks(range(160, 360, 40))#设置y轴显示范围以及间隔
ax.set_ylabel('OLR(w/m$^2$)',fontsize=15,color='r')

ax.tick_params(axis='y',which='minor', length=5,color='r')
ax.tick_params(which='major', width=1.0,length=10)
ax.yaxis.set_minor_locator(AutoMinorLocator(2))
ax.xaxis.set_minor_locator(AutoMinorLocator(2))
ax.set_title('SST and OLR',fontsize=20)

# ax = sns.regplot(x="z", y="zz")

                
#共用x轴，再画一个y

ax2 = ax.twinx()
ax2.tick_params( axis='y',direction='out',
          labelsize=15)#设置y轴颜色，外凸间隔，字体大小
ax2.spines['left'].set_color ('r')
ax2.plot(x,num10,'k')
ax2.set_ylabel('log$_1$$_0$(Numbers)',fontsize=15)
ax2.yaxis.set_minor_locator(AutoMinorLocator(2))
ax2.tick_params(which='minor', length=5)
ax2.tick_params(which='major', width=1.0,length=10)
ax2.tick_params(direction='out', axis='y',
          labelsize=15, grid_alpha=0.5)     
ax2.set_yticks(range(1, 6, 1)) 


ax3.plot(z,c_rate_mean,'b')
ax3.invert_yaxis()
ax3.set_xlim(20,32)
# ax3.set_ylim(320,160)
ax3.grid(linestyle='--')
ax3.grid(linestyle='--',which='minor',axis='x',alpha=0.75)
ax3.xaxis.set_minor_locator(AutoMinorLocator(2))
ax3.yaxis.set_minor_locator(AutoMinorLocator(2))
ax3.tick_params(axis='y',which='minor', length=5)
ax3.tick_params(axis='y',which='major', length=10)
ax3.tick_params(axis='x',which='minor', length=5)
ax3.tick_params(axis='x',which='major', length=10)
ax3.set_xlabel('SST(°C)',fontsize=15)
ax3.set_ylabel('Changing rate(w/m$^2$/°C)',fontsize=15)
ax3.set_title(' $\partial $OLR/$\partial $SST',fontsize=20)


    
    