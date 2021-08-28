# -*- coding: utf-8 -*-
"""
Created on Fri Aug 27 16:08:24 2021

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
# p='/mnt/h/select/'
path1='D:\\desktopppp\\sst_olr\\interp_nan\\olr_1982_2012.nc'
ds=xr.open_dataset(path1)
path2='D:\\desktopppp\\sst_olr\\interp_nan\\sst_interp_1982_2012.nc'
da = xr.open_dataset(path2)
path3='D:\\desktopppp\\sst_olr\\interp_nan\\hadv_interp_0814.nc'

patholr='D:\\desktopppp\\olr_mean.csv'

dolr=pd.read_csv(patholr)

#==================读取olr均值、olr随sst变化率====================
olr_0mse_mean=np.array(dolr['0mse'])#olr均值
dh=xr.open_dataset(path3)
lon=np.array(ds['lon'])
lat=np.array(ds['lat'])
time=ds['time']
time=time.loc['1982':'2012'][:]
lat_range = lat[(lat>-22.5) & (lat<22.5)]

olr_region =ds.sel(lon=lon, lat=lat_range,time=time).olr
olr_region_mean =np.array(olr_region.mean('time', skipna=True))

sst_region_mean =np.array(da.sel(lon=lon, lat=lat_range,time=time).sst)
# sst_region_mean =np.array(sst_region.mean('time', skipna=True))

hadv_region =dh.sel(lon=lon, lat=lat_range,time=time).hadv
hadv_region_mean =np.array(hadv_region.mean('time', skipna=True))
act=np.full((372,17,144),0.0)
index1=(sst_region_mean>=25.25)&(sst_region_mean<=28.75)
index2=(sst_region_mean<=29.5)&(sst_region_mean>=28.75)
index3=sst_region_mean<25.25
index4=sst_region_mean>29.5
sst1=sst_region_mean[index1]
sst2=sst_region_mean[index2]

sst2.shape
a=-4.31972
b=110.55619
x=[]
x2=[]
for i in range(len(sst1)):
    x.append(np.trapz([25.25*a+b,sst1[i]*a+b]))
a1=23.13986
b1=-683.50776
for k in range(len(sst2)):
    x2.append(np.trapz([28.75*a1+b1,sst2[k]*a1+b1]))
x=x+olr_0mse_mean[21]
x2=x2+x[-1]
act[index1]=x
act[index2]=x2
act[index3]=olr_0mse_mean[21]
act[index4]=x2[-1]

np.save(file="act_data.npy", arr=act)
#b= np.load(file="data.npy")

# fig=plt.figure(figsize=(15,10))
# plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
# plt.rcParams['font.sans-serif']=['Fangsong']
# ax=fig.add_subplot(411,projection=ccrs.PlateCarree(central_longitude=180))
# cb=ax.contourf(lon,lat_range,act[0],levels=np.arange(240,270),cmap=plt.get_cmap('bwr'),    \
#             transform=ccrs.PlateCarree()) 
# # c=contour = plt.contour(lon,lat_range, sst_region_mean,10,colors='grey',zorder=1,\
# #                               transform=ccrs.PlateCarree())

# ax.add_feature(cfeature.NaturalEarthFeature('physical', 'land', '50m', \
#                                             edgecolor='white', facecolor='white',zorder=2))
# ax.set_xticks(np.arange(-180, 210, 45),crs=ccrs.PlateCarree(central_longitude=180))
# ax.set_yticks(np.arange(-20, 20+10, 10),crs=ccrs.PlateCarree())
# ax.xaxis.set_major_formatter(LongitudeFormatter())
# ax.yaxis.set_major_formatter(LatitudeFormatter())
# ax.set_title('ACT 平均态水平分布图',fontsize=15)
# ax.set_xlabel('经度($°$)',fontsize=15)
# ax.set_ylabel('纬度($°$)',fontsize=15)
# cbar = plt.colorbar(cb,shrink=0.6,ticks=[240,260],aspect=5,pad=0.01)