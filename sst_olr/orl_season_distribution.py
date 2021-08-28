# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 09:07:55 2021

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
path2='D:\\desktopppp\\sst_olr\\sst.mnmean.nc'
da = xr.open_dataset(path2)
ds=xr.open_dataset(path1)
# sst = ds['sst']
# sst= sst.interp(lat=orl.lat.values, lon=orl.lon.values,kwargs={  "fill_value": "extrapolate"})
lon=ds['lon'][:]
lat=ds['lat']
time=ds['time'][:]
time=time.loc['1982':'2012'][:]


lat_range = lat[(lat>-22.5) & (lat<22.5)]
orl_region =ds.sel(lon=lon, lat=lat_range,time=time)
season_summary = orl_region.groupby(
    'time.season').mean('time', skipna=True)
#=====================draw==================================================
JJA=season_summary['olr'][1]
fig=plt.figure(figsize=(20,12))#设置一个画板，将其返还给fig
# fig.suptitle('OLR seasonnal distribution')
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 15
# plt.title('OLR distribution')
ax = fig.add_subplot(4, 1, 1, projection=ccrs.PlateCarree(central_longitude=180))
ax.coastlines()
# ax.contourf(lon_range,lat_range,season_summary['olr'][0])

cycle_olr, cycle_lon = add_cyclic_point(JJA, coord=lon)
cycle_LON, cycle_LAT = np.meshgrid(cycle_lon, lat_range)
cb=ax.contourf(cycle_LON,cycle_LAT, cycle_olr,levels=np.arange(200,300),cmap = "RdBu_r",\
   zorder=0,transform=ccrs.PlateCarree())
contour = plt.contour(cycle_LON,cycle_LAT, cycle_olr,colors='k',zorder=1,transform=ccrs.PlateCarree())
ax.add_feature(cfeature.NaturalEarthFeature('physical', 'land', '110m', \
                                            edgecolor='white', facecolor='white',zorder=2))#zorder 显示图层叠加顺序

ax.set_xticks(np.arange(0, 361, 30),crs=ccrs.PlateCarree())
ax.set_yticks(np.arange(-20, 40, 20),crs=ccrs.PlateCarree())
ax.xaxis.set_major_formatter(LongitudeFormatter())#经度0度不加东西
ax.yaxis.set_major_formatter(LatitudeFormatter())
# cm = plt.cm.get_cmap('Spectral')#Spectral_r
ax.set_title('JJA-OLR horizontal distribution')
cbar = plt.colorbar(cb,shrink=0.7,pad=0.04,ticks=[200,250],aspect=3.5)
################################################################################
ax1 = fig.add_subplot(4, 1, 2, projection=ccrs.PlateCarree(central_longitude=180))#中心线
ax1.add_feature(cfeature.NaturalEarthFeature('physical', 'land', '110m', \
                                            edgecolor='black', facecolor='white'))
cycle_sst1, cycle_lon = add_cyclic_point(season_summary['olr'][2], coord=lon)
cycle_LON, cycle_LAT = np.meshgrid(cycle_lon, lat_range)
cb=ax1.contourf(cycle_LON,cycle_LAT, cycle_sst1,levels=np.arange(200,300),cmap = "RdBu_r",\
 zorder=0 ,transform=ccrs.PlateCarree()  )
contour = plt.contour(cycle_LON,cycle_LAT, cycle_sst1,colors='k',zorder=1,transform=ccrs.PlateCarree())
ax1.add_feature(cfeature.NaturalEarthFeature('physical', 'land', '110m', \
                                            edgecolor='white', facecolor='white',zorder=2))

ax1.set_xticks(np.arange(0, 361, 30),crs=ccrs.PlateCarree())
ax1.set_yticks(np.arange(-20, 40, 20),crs=ccrs.PlateCarree())
ax1.xaxis.set_major_formatter(LongitudeFormatter(zero_direction_label = False))#经度0度不加东西
ax1.yaxis.set_major_formatter(LatitudeFormatter())
# cm = plt.cm.get_cmap('bwr')#Spectral_r
ax1.set_title('MAM-OLR horizontal distribution')
cbar = plt.colorbar(cb,shrink=0.7,pad=0.04,ticks=[200,250],aspect=3.5)
#===============================================================================
ax2= fig.add_subplot(4, 1, 3, projection=ccrs.PlateCarree(central_longitude=180))#中心线
ax2.add_feature(cfeature.NaturalEarthFeature('physical', 'land', '110m', \
                                            edgecolor='black', facecolor='white'))
cycle_sst2, cycle_lon = add_cyclic_point(season_summary['olr'][3], coord=lon)
cycle_LON, cycle_LAT = np.meshgrid(cycle_lon, lat_range)
cb=ax2.contourf(cycle_LON,cycle_LAT, cycle_sst2,levels=np.arange(200,300),cmap = "RdBu_r",\
 zorder=0  ,transform=ccrs.PlateCarree() )
contour = plt.contour(cycle_LON,cycle_LAT, cycle_sst2,colors='k',zorder=1,transform=ccrs.PlateCarree())
ax2.add_feature(cfeature.NaturalEarthFeature('physical', 'land', '110m', \
                                            edgecolor='white', facecolor='white',zorder=2))

ax2.set_xticks(np.arange(0, 361, 30),crs=ccrs.PlateCarree())
ax2.set_yticks(np.arange(-20, 40, 20),crs=ccrs.PlateCarree())
ax2.xaxis.set_major_formatter(LongitudeFormatter(zero_direction_label = False))#经度0度不加东西
ax2.yaxis.set_major_formatter(LatitudeFormatter())
# cm = plt.cm.get_cmap('bwr')#Spectral_r
ax2.set_title('SON-OLR horizontal distribution')
cbar = plt.colorbar(cb,shrink=0.7,pad=0.04,ticks=[200,250],aspect=3.5)
#==============================================================
ax3= fig.add_subplot(4, 1, 4, projection=ccrs.PlateCarree(central_longitude=180))#中心线
ax3.add_feature(cfeature.NaturalEarthFeature('physical', 'land', '110m', \
                                            edgecolor='black', facecolor='white'))
cycle_sst3, cycle_lon = add_cyclic_point(season_summary['olr'][0], coord=lon)
cycle_LON, cycle_LAT = np.meshgrid(cycle_lon, lat_range)
cb=ax3.contourf(cycle_LON,cycle_LAT, cycle_sst3,levels=np.arange(200,300),cmap = "RdBu_r",\
  zorder=0  ,transform=ccrs.PlateCarree())
contour = plt.contour(cycle_LON,cycle_LAT, cycle_sst3,colors='k',zorder=1,transform=ccrs.PlateCarree())
ax3.add_feature(cfeature.NaturalEarthFeature('physical', 'land', '110m', \
                                            edgecolor='white', facecolor='white',zorder=2))

ax3.set_xticks(np.arange(0, 361, 30),crs=ccrs.PlateCarree())
ax3.set_yticks(np.arange(-20, 40, 20),crs=ccrs.PlateCarree())
ax3.xaxis.set_major_formatter(LongitudeFormatter(zero_direction_label = False))#经度0度不加东西
ax3.yaxis.set_major_formatter(LatitudeFormatter())
# cm = plt.cm.get_cmap('bwr')#Spectral_r
ax3.set_title('DJF-OLR horizontal distribution')
cbar = plt.colorbar(cb,shrink=0.7,pad=0.04,ticks=[200,250],aspect=3.5)

fig.savefig('D:\\desktopppp\\sst_olr\\picture\\'+'olr_horizontal_distribution.tiff',format='tiff',dpi=150)
