# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 22:20:52 2021

@author: 纪
"""
import cartopy.feature as cfeature
from cartopy.util import add_cyclic_point
import matplotlib.ticker as mticker
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import pandas as pd
from netCDF4 import num2date
import cmaps
import matplotlib.pyplot as plt
import numpy as np
import netCDF4 as nc
import cartopy.crs as ccrs
import os
import numpy as np
import xarray as xr

path='D:\\desktopppp\\sst_olr\\interp_nan\\sst_interp_1982_2012.nc'

sst=xr.open_dataset(path)
lon=sst.lon
lat=sst.lat
lat_range = lat[(lat>-22.5) & (lat<22.5)]
sst_region =sst.sel(lat=lat_range,lon=lon)
season =sst_region.groupby(
    'time.season').mean('time', skipna=True)
#=====================draw==============================================
fig=plt.figure(figsize=(20,12))#设置一个画板，将其返还给fig

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 15

ax = fig.add_subplot(4, 1, 1, projection=ccrs.PlateCarree(central_longitude =180))
ax.add_feature(cfeature.NaturalEarthFeature('physical', 'land', '50m', \
                                            edgecolor='white', facecolor='white',zorder=2))
cycle_sst, cycle_lon = add_cyclic_point(season.sst[1], coord=lon)
cycle_LON, cycle_LAT = np.meshgrid(cycle_lon, lat_range)
cb=ax.contourf(cycle_LON,cycle_LAT, cycle_sst,levels=np.arange(20,36),cmap='bwr',\
   zorder=0,transform= ccrs.PlateCarree())
ax.set_xticks(np.arange(0, 361, 30),crs=ccrs.PlateCarree())
ax.set_yticks(np.arange(-20, 40, 20),crs=ccrs.PlateCarree())
ax.xaxis.set_major_formatter(LongitudeFormatter(zero_direction_label =False))#经度0不加标识
ax.yaxis.set_major_formatter(LatitudeFormatter())

contour = ax.contour(lon,lat_range, season.sst[1],colors='k',zorder=1,transform= ccrs.PlateCarree())
#zorder 显示图层叠加顺序

ax.tick_params(which='major', direction='out', length=10, width=0.99, pad=0.2, bottom=True, left=True, right=False, top=False)
ax.set_title('JJA-SST horizontal distribution')

cbar = fig.colorbar(cb,shrink=0.7,ticks=[20,25,30],pad=0.04,aspect=3.5)

##########################################################################
ax1 = fig.add_subplot(4, 1, 2, projection=ccrs.PlateCarree(central_longitude=180))#中心线
ax1.add_feature(cfeature.NaturalEarthFeature('physical', 'land', '110m', \
                                            edgecolor='black', facecolor='white'))
cycle_sst1, cycle_lon = add_cyclic_point(season.sst[2], coord=lon)
cb=ax1.contourf(cycle_LON,cycle_LAT, cycle_sst1,levels=np.arange(20,34),cmap='bwr',\
    zorder=0,transform= ccrs.PlateCarree() )

contour = plt.contour(cycle_LON,cycle_LAT, cycle_sst1,colors='k',zorder=1,transform= ccrs.PlateCarree())
ax1.add_feature(cfeature.NaturalEarthFeature('physical', 'land', '50m', \
                                            edgecolor='white', facecolor='white',zorder=2))

ax1.tick_params(which='major', direction='out', length=10, width=0.99, pad=0.2, bottom=True, left=True, right=False, top=False)
ax1.set_xticks(np.arange(0, 361, 30),crs=ccrs.PlateCarree())
ax1.set_yticks(np.arange(-20, 40, 20),crs=ccrs.PlateCarree())
ax1.xaxis.set_major_formatter(LongitudeFormatter(zero_direction_label =False))#经度0不加标识
ax1.yaxis.set_major_formatter(LatitudeFormatter())
ax1.set_title('MAM-SST horizontal distribution')
cbar = fig.colorbar(cb,shrink=0.7,ticks=[20,25,30],pad=0.04,aspect=3.5)
#============================================================================
ax2= fig.add_subplot(4, 1, 3, projection=ccrs.PlateCarree(central_longitude=180))#中心线
ax2.add_feature(cfeature.NaturalEarthFeature('physical', 'land', '110m', \
                                            edgecolor='black', facecolor='white'))
cycle_sst2, cycle_lon = add_cyclic_point(season.sst[3], coord=lon)
cb=ax2.contourf(cycle_LON,cycle_LAT, cycle_sst2,levels=np.arange(20,34),cmap='bwr',\
   zorder=0,transform= ccrs.PlateCarree()  )
contour = plt.contour(cycle_LON,cycle_LAT, cycle_sst2,colors='k',zorder=1,transform= ccrs.PlateCarree())
ax2.add_feature(cfeature.NaturalEarthFeature('physical', 'land', '50m', \
 edgecolor='white', facecolor='white',zorder=2))

ax2.tick_params(which='major', direction='out', length=10, width=0.99, pad=0.2, bottom=True, left=True, right=False, top=False)
ax2.set_xticks(np.arange(0, 361, 30),crs=ccrs.PlateCarree())
ax2.set_yticks(np.arange(-20, 40, 20),crs=ccrs.PlateCarree())
ax2.xaxis.set_major_formatter(LongitudeFormatter(zero_direction_label =False))#经度0不加标识
ax2.yaxis.set_major_formatter(LatitudeFormatter())
ax2.set_title('SON-SST horizontal distribution')
cbar = fig.colorbar(cb,shrink=0.7,ticks=[20,25,30],pad=0.04,aspect=3.5)
#============================================================================
ax3= fig.add_subplot(4, 1, 4, projection=ccrs.PlateCarree(central_longitude=180))#中心线
ax3.add_feature(cfeature.NaturalEarthFeature('physical', 'land', '110m', \
                                            edgecolor='black', facecolor='white'))
cycle_sst3, cycle_lon = add_cyclic_point(season.sst[0], coord=lon)
cb=ax3.contourf(cycle_LON,cycle_LAT, cycle_sst3,levels=np.arange(20,34),cmap='bwr',\
    zorder=0,transform= ccrs.PlateCarree() )
contour = plt.contour(cycle_LON,cycle_LAT, cycle_sst3,colors='k',zorder=1,transform= ccrs.PlateCarree())
ax3.add_feature(cfeature.NaturalEarthFeature('physical', 'land', '50m', \
                                            edgecolor='white', facecolor='white',zorder=2))

ax3.tick_params(which='major', direction='out', length=10, width=0.99, pad=0.2, bottom=True, left=True, right=False, top=False)
ax3.set_xticks(np.arange(0, 361, 30),crs=ccrs.PlateCarree())
ax3.set_yticks(np.arange(-20, 40, 20),crs=ccrs.PlateCarree())
ax3.xaxis.set_major_formatter(LongitudeFormatter(zero_direction_label =False))#经度0不加标识
ax3.yaxis.set_major_formatter(LatitudeFormatter())
ax3.set_title('DJF-SST horizontal distribution')
cbar = fig.colorbar(cb,shrink=0.7,ticks=[20,25,30],pad=0.04,aspect=3.5)

fig.savefig('D:\\desktopppp\\sst_olr\\picture\\'+'SST_horizontal_distribution.tiff',format='tiff',dpi=150)
