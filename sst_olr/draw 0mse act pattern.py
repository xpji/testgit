# -*- coding: utf-8 -*-
"""
Created on Thu Aug 26 15:03:36 2021

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

sst_region =da.sel(lon=lon, lat=lat_range,time=time).sst
sst_region_mean =np.array(sst_region.mean('time', skipna=True))

hadv_region =dh.sel(lon=lon, lat=lat_range,time=time).hadv
hadv_region_mean =np.array(hadv_region.mean('time', skipna=True))
act=np.full((17,144),0.0)
# ##========挑选0MSE的sst \ OLR=====
# # # # # 挑选0mse SST 中的符合模型的数据，分为两部分
for i in sst_region_mean:
    idx=(sst_region_mean>=25.2500)&(sst_region_mean<=28.7500)
    idx1=(sst_region_mean<=29.500)&(sst_region_mean>=28.7500)
    sst_1=sst_region_mean[idx]
    sst_2=sst_region_mean[idx1]
# # # # #模型中的系数：EOT=a*sst+b 
a=-4.31972
b=110.55619
# # #计算eot第一段中sst1中act值
act1=[]
for j in range(len(sst_1)):
    x=sst_1[j]
    # print(j)
    act1.append(np.trapz([25.250*a+b,x*a+b],x=[25.250,sst_1[j]]))

act1=act1+olr_0mse_mean[21]
act2=[]
a1=23.13986
b1=-683.50776
for k in range(len(sst_2)):
    xx=sst_2[k]
    act2.append(np.trapz([28.750*a1+b1,xx*a1+b1],x=[28.750,sst_2[k]]))
act2=act2+act1[-1]
# # #=====================
act0=[]
act3=[]

idx0=sst_region_mean<=25.25
idx2=sst_region_mean<=25.25
act[idx0]=olr_0mse_mean[21]
act[idx]=act1
act[idx1]=act2
act[idx2]=act2[-1]
# # # # # #==============================================================================
# act_0mse[idx]=act1
# act_0mse[idx1]=act2
# act_0mse[idx2]=act0
# act_0mse[idx3]=act3
# act_0mse[act_0mse==0]=np.nan
# act[indx]=act_0mse
act[act==0]=np.nan

# # # # #==============================draw ACT==================================
fig=plt.figure(figsize=(15,8))
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
plt.rcParams['font.sans-serif']=['Fangsong']
ax=fig.add_subplot(211,projection=ccrs.PlateCarree(central_longitude=180))
# ax.contourf(lon,lat_range,act,levels=np.arange(250,280))
cycle_act, cycle_lon = add_cyclic_point(act, coord=lon)

cycle_LON, cycle_LAT = np.meshgrid(cycle_lon, lat_range)
# 
cb=ax.contourf(cycle_LON,cycle_LAT, cycle_act,levels=np.arange(240,270),\
    cmap='RdBu', transform=ccrs.PlateCarree() )
    
contour = plt.contour(cycle_LON,cycle_LAT, cycle_act,colors='grey',zorder=1,\
                       transform=ccrs.PlateCarree())
ax.add_feature(cfeature.NaturalEarthFeature('physical', 'land', '50m', \
                                            edgecolor='white', facecolor='white',zorder=2))
ax.set_xticks(np.arange(-180, 210, 45),crs=ccrs.PlateCarree(central_longitude=180))
ax.set_yticks(np.arange(-20, 20+10, 10),crs=ccrs.PlateCarree())
ax.xaxis.set_major_formatter(LongitudeFormatter())
ax.yaxis.set_major_formatter(LatitudeFormatter())
ax.set_title('ACT 平均态水平分布图',fontsize=15)
ax.set_xlabel('经度($°$)',fontsize=15)
ax.set_ylabel('纬度($°$)',fontsize=15)
cbar = plt.colorbar(cb,shrink=0.4,ticks=[240,250,260],aspect=5,pad=0.01)
# #==============================================================================
ax1=fig.add_subplot(212,projection=ccrs.PlateCarree(central_longitude=180))
cycle_olr, cycle_lon = add_cyclic_point(olr_region_mean, coord=lon)

cycle_LON, cycle_LAT = np.meshgrid(cycle_lon, lat_range)

cb=ax1.contourf(cycle_LON,cycle_LAT, cycle_olr,levels=np.arange(200,280),\
  cmap='RdBu',  zorder=0, transform=ccrs.PlateCarree())
    
contour = plt.contour(cycle_LON,cycle_LAT, cycle_olr,colors='grey',zorder=1,\
                       transform=ccrs.PlateCarree())

ax1.add_feature(cfeature.NaturalEarthFeature('physical', 'land', '50m', \
                                            edgecolor='white', facecolor='white',zorder=2))
ax1.set_xticks(np.arange(-180, 210, 45),crs=ccrs.PlateCarree(central_longitude=180))
ax1.set_yticks(np.arange(-20, 30, 10),crs=ccrs.PlateCarree())
ax1.xaxis.set_major_formatter(LongitudeFormatter())#经度0度不加东西
ax1.yaxis.set_major_formatter(LatitudeFormatter())
ax1.set_title('热带海域 OLR 平均态水平分布图',fontsize=15)
ax1.set_xlabel('经度($°$)',fontsize=15)
ax1.set_ylabel('纬度($°$)',fontsize=15)
cbar = plt.colorbar(cb,shrink=0.5,ticks=[200,250],aspect=5,pad=0.01)
