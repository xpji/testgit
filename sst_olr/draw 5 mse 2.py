# -*- coding: utf-8 -*-
"""
Created on Fri Aug 27 10:00:06 2021

@author: 纪
"""



import pandas as pd
import cartopy.feature as cfeature
from cartopy.util import add_cyclic_point
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy as np
import xarray as xr
path3='D:\\desktopppp\\sst_olr\\interp_nan\\hadv_interp_0814.nc'
dh=xr.open_dataset(path3)
lon=np.array(dh['lon'])
lat=np.array(dh['lat'])
time=dh['time']
time=time.loc['1982':'2012'][:]
lat_range = lat[(lat>-22.5) & (lat<22.5)]
hadv_region =dh.sel(lon=lon, lat=lat_range,time=time).hadv
hadv =np.array(hadv_region.mean('time', skipna=True))
hadv_range=np.arange(-125,125+50,50)
indx=[]
lon=hadv_region.lon
lat=hadv_region.lat
index1 = np.argwhere((hadv<25) & (hadv > -25))
lonr=lon[index1[:,1]]
latr=lat[index1[:,0]]


fig=plt.figure(figsize=(20,12))
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
plt.rcParams['font.sans-serif']=['Fangsong']
ax=fig.add_subplot(211,projection=ccrs.PlateCarree(central_longitude=180))
ax.scatter(lonr,latr,marker='o',c='g',transform=ccrs.PlateCarree(central_longitude=180))
# # 挑选 不同的bin 



ax.coastlines()
ax.set_xticks(np.arange(-180, 210, 45),crs=ccrs.PlateCarree(central_longitude=180))
ax.set_yticks(np.arange(-20, 30, 10),crs=ccrs.PlateCarree())
ax.xaxis.set_major_formatter(LongitudeFormatter())#经度0度不加东西
ax.yaxis.set_major_formatter(LatitudeFormatter())
ax.set_title('热带海域 MSE 空间水平分布图',fontsize=20)
ax.set_xlabel('经度($°$)',fontsize=20)
ax.set_ylabel('纬度($°$)',fontsize=20)
ax.add_feature(cfeature.NaturalEarthFeature('physical', 'land', '50m', \
                                            edgecolor='black', facecolor='grey'))

# fig.savefig(path+'SMAP vs Argo error distribution.svg',format='svg',dpi=150)