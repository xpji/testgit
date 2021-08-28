# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 22:16:08 2021

@author: 纪
"""
from matplotlib.ticker import FuncFormatter 
import seaborn as sns
from xhistogram.xarray import histogram as xhistogram
from scipy.optimize import curve_fit
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
from scipy.optimize import leastsq
from itertools import groupby
import xarray as xr
import netCDF4 as nc
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import glob
import cartopy.crs as ccrs

path='D:\\desktopppp\\sst_olr\\interp_nan\\hadv_interp_0814.nc'
hadv=xr.open_dataset(path)
path0='D:\\desktopppp\\sst_olr\\interp_nan\\sst_interp_1982_2012.nc'
ds=xr.open_dataset(path0)
lat=ds['lat']
time=ds['time']
time=time.loc['1982':'2012']
lon=np.array(ds['lon'])
lat_range= lat[(lat>-22.5) & (lat<22.5)]
lon_range=lon[(lon>=120)&(lon<=260)]
sst=ds.sel(lat=lat_range)
sst=sst['sst']
hadv=hadv.sel(lat=lat_range)['hadv']

ha=np.array(hadv).flatten()

def formatnum(x, pos):
    return '$%.0d$' % (x/10000)   #注意修改两处的值，一个为x的除数，一个为对应的指数
# %是一个特殊的操作符，该操作符会将后面的变量值，替换掉前面字符串中的占位符。f:十进制浮点数(小数), 自动保留六位小数。
fig=plt.figure(dpi=150,figsize=(20,5))
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
ax=fig.add_subplot(131)

n,bins,patches=ax.hist(ha,400,align='mid')

formatter = FuncFormatter(formatnum)
ax.yaxis.set_major_formatter(formatter)
# ax.yaxis.get_major_formatter().set_powerlimits((0,1))
ax.set_title('x10$^4$',loc='left')
ax.set_xlabel('MSE平流强度(w/m$^2$)')
ax.set_ylabel('频 数')
ax.set_title('各MSE平流强度数据点频数直方图',y=1.05)#参数y将其向上移动
ax.set_xlim(-400, 400)
#==================draw 热带海域全数据点============================
ax1=fig.add_subplot(132)
ax1.scatter(sst,hadv,s=1)
ax1.set_ylim(-600,600)
ax1.set_xlim(14,34)
ax1.set_xticks(np.linspace(14,34,6))
ax1.set_xlabel('Sea Surface Temperature($^°$C)')
ax1.set_ylabel('MSE平流强度(w/m$^2$)')
ax1.set_title('热带海域全数据点',pad=20)#pad表示标题与画布之间的填充
ax1.spines['right'].set_visible(False)
ax1.spines['top'].set_visible(False)

#=====================================================================

ax2=fig.add_subplot(133)
bins = np.linspace(-400, 400, 81)
h = (xhistogram(hadv, bins=[bins]))

hb=h/10000
hb.plot()
# formatter = FuncFormatter(formatnum)
# ax2.yaxis.set_major_formatter(formatter)
ax2.yaxis.get_major_formatter().set_powerlimits((0,1)) # 将坐标轴的base number设置为一位。
ax2.set_title('x10$^4$',loc='left')
ax2.set_xlabel('MSE平流强度(w/m$^2$)')
ax2.set_ylabel('频 数')
ax2.set_title('各MSE平流强度数据点频数折线图',y=1.05)
ax2.set_xlim(-400, 400)
ax2.set_ylim(0,9)


fig.savefig('D:\\desktopppp\\sst_olr\\picture\\'+'热带海域全数据点.tiff',format='tiff',dpi=150)
