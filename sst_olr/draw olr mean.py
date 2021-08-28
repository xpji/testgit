# -*- coding: utf-8 -*-
"""
Created on Fri Aug 27 12:45:54 2021

@author: 纪
"""
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy as np
import xarray as xr
from cartopy.mpl.ticker import LongitudeFormatter,LatitudeFormatter
file = xr.open_dataset('D:\\desktopppp\\sst_olr\\olr.mon.mean.nc')
time=file['time']
time=time.loc['1982':'2012'][:]
lat = file["lat"].data
lon = file["lon"].data
lat_range = lat[(lat>-22.5) & (lat<22.5)]
olr_region =file.sel(lon=lon, lat=lat_range,time=time).olr
mean =np.array(olr_region.mean('time', skipna=True))
levels = np.arange(200,280)
box = [0, 361, -20, 20]  
xstep, ystep = 30, 10    
cmap = "bwr"

fig = plt.figure(figsize=(20,12))
ax = fig.add_subplot(111,projection=ccrs.PlateCarree(central_longitude=180))

p = ax.contourf(lon,
                lat_range,
                mean,
                cmap=cmap,
                levels=levels,
                # extend='both',
                zorder=0,
                transform=ccrs.PlateCarree())
contour = plt.contour(lon,lat_range, mean,colors='grey',zorder=1,transform=ccrs.PlateCarree())
ax.add_feature(cfeature.NaturalEarthFeature('physical', 'land', '50m', \
                                            edgecolor='white', facecolor='white',zorder=2))
ax.set_xticks(np.arange(-180, 210, 45),crs=ccrs.PlateCarree(central_longitude=180))
ax.set_yticks(np.arange(-20, 20+10, 10),crs=ccrs.PlateCarree())
ax.xaxis.set_major_formatter(LongitudeFormatter())
ax.yaxis.set_major_formatter(LatitudeFormatter())
ax.set_title('热带海域 OLR 平均态水平分布图',fontsize=15)
ax.set_xlabel('经度($°$)',fontsize=15)
ax.set_ylabel('纬度($°$)',fontsize=15)
cbar = plt.colorbar(p,shrink=0.15,pad=0.03,aspect=5,ticks=[200,250])

# fig.savefig('D:\\desktopppp\\sst_olr\\picture\\'+'热带海域 OLR 平均态水平分布图.tiff',format='tiff',dpi=150)