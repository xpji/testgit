# -*- coding: utf-8 -*-
"""
Created on Fri Aug 27 21:17:22 2021

@author: 纪
"""

import pandas as pd
import cartopy.feature as cfeature
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
dh = xr.open_dataset(path3)
dolr=pd.read_csv(patholr)
olr_0mse_mean=np.array(dolr['0mse'])#olr均值
olr_time=ds.time
lon=ds.lon
time_range=olr_time.loc['2012-6'][:]
lat_range = ds.lat[(ds.lat>-22.5) & (ds.lat<22.5)]
olr=ds.sel(time=time_range,lat=lat_range).olr
hadv=dh.sel(time=time_range,lat=lat_range).hadv
sst=da.sel(time=time_range,lat=lat_range).sst.data

act=np.full((17,144),0.0)
index1=(sst>=25.25)&(sst<=28.75)[0]
index2=(sst<=29.5)&(sst>=28.75)[0]
index3=(sst<25.25)[0]
index4=(sst>29.5)[0]
sst1=sst[index1]
sst2=sst[index2]


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
act[index1[0]]=x
act[index2[0]]=x2
act[index3]=olr_0mse_mean[21]
act[index4]=x2[-1]
act[act==0.0]=np.nan
fig=plt.figure(figsize=(15,10))
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
plt.rcParams['font.sans-serif']=['Fangsong']
#==============================================================================
ax=fig.add_subplot(411,projection=ccrs.PlateCarree(central_longitude=180))
cb=ax.contourf(lon,lat_range,act,levels=np.arange(245,270),cmap=plt.get_cmap('RdBu_r'),    \
            transform=ccrs.PlateCarree(),zorder=0) 
c= plt.contour(lon,lat_range, act,5,colors='grey',zorder=1,\
                              transform=ccrs.PlateCarree())
ax.add_feature(cfeature.NaturalEarthFeature('physical', 'land', '50m', \
       edgecolor='white', facecolor='white',zorder=2))
ax.set_xticks(np.arange(-180, 210, 45),crs=ccrs.PlateCarree(central_longitude=180))
ax.set_yticks(np.arange(-20, 20+10, 10),crs=ccrs.PlateCarree())
ax.xaxis.set_major_formatter(LongitudeFormatter())
ax.yaxis.set_major_formatter(LatitudeFormatter())
ax.set_title('2012年6月热带海域 ACT 平均态水平分布图',fontsize=15)
ax.set_xlabel('经度($°$)',fontsize=15)
ax.set_ylabel('纬度($°$)',fontsize=15)
cbar = plt.colorbar(cb,shrink=0.6,ticks=[245,255,265,270],aspect=5,pad=0.01)
#==============================================================================
ax1=fig.add_subplot(412,projection=ccrs.PlateCarree(central_longitude=180))
cb=ax1.contourf(lon,lat_range, olr[0],levels=np.arange(180,280),\
  cmap='RdBu_r',  zorder=0,       transform=ccrs.PlateCarree())
    
contour = plt.contour(lon,lat_range, olr[0],colors='grey',zorder=1,\
                              transform=ccrs.PlateCarree())
ax1.add_feature(cfeature.NaturalEarthFeature('physical', 'land', '50m', \
                                            edgecolor='white', facecolor='white',zorder=2))
ax1.set_xticks(np.arange(-180, 210, 45),crs=ccrs.PlateCarree(central_longitude=180))
ax1.set_yticks(np.arange(-20, 30, 10),crs=ccrs.PlateCarree())
ax1.xaxis.set_major_formatter(LongitudeFormatter())#经度0度不加东西
ax1.yaxis.set_major_formatter(LatitudeFormatter())
ax1.set_title('2012年6月热带海域 OLR 平均态水平分布图',fontsize=15)
ax1.set_xlabel('经度($°$)',fontsize=15)
ax1.set_ylabel('纬度($°$)',fontsize=15)
cbar = plt.colorbar(cb,shrink=0.6,ticks=[180,220,260],aspect=5,pad=0.01)
#---==================================================================
ax2=fig.add_subplot(413,projection=ccrs.PlateCarree(central_longitude=180))
cb=ax2.contourf(lon,lat_range, olr[0]-act,levels=np.arange(-60,25),\
  cmap='RdBu_r',  zorder=0,       transform=ccrs.PlateCarree())
    
contour = plt.contour(lon,lat_range, olr[0]-act,colors='grey',zorder=1,\
                              transform=ccrs.PlateCarree())

ax2.add_feature(cfeature.NaturalEarthFeature('physical', 'land', '50m', \
                                            edgecolor='white', facecolor='white',zorder=2))
ax2.set_xticks(np.arange(-180, 210, 45),crs=ccrs.PlateCarree(central_longitude=180))
ax2.set_yticks(np.arange(-20, 30, 10),crs=ccrs.PlateCarree())
ax2.xaxis.set_major_formatter(LongitudeFormatter())#经度0度不加东西
ax2.yaxis.set_major_formatter(LatitudeFormatter())
ax2.set_title('2012年6月热带海域 OLR-ACT 平均态水平分布图',fontsize=15)
ax2.set_xlabel('经度($°$)',fontsize=15)
ax2.set_ylabel('纬度($°$)',fontsize=15)
cbar = plt.colorbar(cb,shrink=0.6,ticks=[-60,-40,-20,0,20],aspect=5,pad=0.01)
#================================================
ax3=fig.add_subplot(414,projection=ccrs.PlateCarree(central_longitude=180))
cb=ax3.contourf(lon,lat_range, hadv[0],levels=np.arange(-200,210),\
  cmap='RdBu_r',  zorder=0,       transform=ccrs.PlateCarree())
    
contour = plt.contour(lon,lat_range, hadv[0],colors='grey',zorder=1,\
                              transform=ccrs.PlateCarree())

ax3.add_feature(cfeature.NaturalEarthFeature('physical', 'land', '50m', \
                                            edgecolor='white', facecolor='white',zorder=2))
ax3.set_xticks(np.arange(-180, 210, 45),crs=ccrs.PlateCarree(central_longitude=180))
ax3.set_yticks(np.arange(-20, 30, 10),crs=ccrs.PlateCarree())
ax3.xaxis.set_major_formatter(LongitudeFormatter())#经度0度不加东西
ax3.yaxis.set_major_formatter(LatitudeFormatter())
ax3.set_title('2012年6月热带海域 MSE 平均态水平分布图',fontsize=15)
ax3.set_xlabel('经度($°$)',fontsize=15)
ax3.set_ylabel('纬度($°$)',fontsize=15)
cbar = plt.colorbar(cb,shrink=0.6,ticks=[-200,0,200],aspect=5,pad=0.01)
# fig.savefig('D:\\desktopppp\\sst_olr\\picture\\'+'2012年6月热带海域估算结果示意图.tiff',format='tiff',dpi=150)