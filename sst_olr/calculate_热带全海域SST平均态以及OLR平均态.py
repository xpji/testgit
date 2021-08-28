# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 20:39:50 2021

@author: 纪
"""

import cartopy.feature as cfeature
from cartopy.util import add_cyclic_point
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy as np
import xarray as xr

path1='D:\\desktopppp\\sst_olr\\olr.mon.mean.nc'
ds=xr.open_dataset(path1)
path2='D:\\desktopppp\\sst_olr\\interp_nan\\sst_interp_1982_2012.nc'
da = xr.open_dataset(path2)
path3='D:\\desktopppp\\sst_olr\\interp_nan\\hadv_interp_0814.nc'
dh=xr.open_dataset(path3)

lon = ds["lon"].data
lat=np.array(ds['lat'])
time=ds['time']
time=time.loc['1982':'2012'][:]
lat_range = lat[(lat>-22.5) & (lat<22.5)]

olr_region =ds.sel(lon=lon, lat=lat_range,time=time)
sst_region =da.sel(lon=lon, lat=lat_range,time=time)
hadv_region =dh.sel(lon=lon, lat=lat_range,time=time)

olr_mean = olr_region.mean('time',skipna=True).olr
sst_mean = sst_region.mean('time', skipna=True).sst
mse_mean = hadv_region.mean('time', skipna=True).hadv


plt.rcParams['font.size'] = 15
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
plt.rcParams['font.sans-serif']=['Fangsong']

levels = np.arange(200,280)
box = [0, 361, -20, 20]  
xstep, ystep = 30, 10    
cmap = "bwr"
# ticks=[240,250,260]
fig = plt.figure(figsize=(20,12))
ax = fig.add_subplot(211,projection=ccrs.PlateCarree(central_longitude=180))
cb=ax.contourf(lon,lat_range,olr_mean,levels=levels,transform=ccrs.PlateCarree(),\
               cmap=cmap,zorder=0)
ax.add_feature(cfeature.NaturalEarthFeature('physical', 'land', '50m', \
                                            edgecolor='w', facecolor='white',zorder=2))
contour = plt.contour(lon,lat_range, olr_mean,zorder=1,colors='grey',transform=ccrs.PlateCarree())
ax.set_xticks(np.arange(0, 360, 45),crs=ccrs.PlateCarree())
ax.set_yticks(np.arange(-20, 30, 10),crs=ccrs.PlateCarree())
ax.xaxis.set_major_formatter(LongitudeFormatter())#经度0度不加东西
ax.yaxis.set_major_formatter(LatitudeFormatter())
ax.set_title('热带海域 OLR 平均态水平分布图',fontsize=20)
ax.set_xlabel('经度($°$)',fontsize=20)
ax.set_ylabel('纬度($°$)',fontsize=20)
cbar = plt.colorbar(cb,shrink=0.4,ticks=[200,250],aspect=4,pad=0.01)
#========================================================================#
#=============================================================================
ax2=fig.add_subplot(212,projection=ccrs.PlateCarree(central_longitude=180))

ch=ax2.contourf(lon,lat_range, sst_mean,levels=np.arange(20,34),cmap='RdBu_r',\
    zorder=0,transform=ccrs.PlateCarree())
contour = plt.contour(lon,lat_range, sst_mean,zorder=1,transform=ccrs.PlateCarree(),colors='grey')
ax2.add_feature(cfeature.NaturalEarthFeature('physical', 'land', '50m', \
                                            edgecolor='white', facecolor='white',zorder=2))
ax2.set_xticks(np.arange(-180, 210, 45),crs=ccrs.PlateCarree(central_longitude=180))
ax2.set_yticks(np.arange(-20, 30, 10),crs=ccrs.PlateCarree())
ax2.xaxis.set_major_formatter(LongitudeFormatter())#经度0度不加东西
ax2.yaxis.set_major_formatter(LatitudeFormatter())
ax2.set_title('热带海域 SST 平流强度平均态水平分布图',fontsize=20)
cobar = plt.colorbar(ch,shrink=0.4,ticks=[20,30],aspect=4,pad=0.01)
ax2.set_xlabel('经度($°$)',fontsize=20)
ax2.set_ylabel('纬度($°$)',fontsize=20)
#=============================================================================
