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

olr_season =np.array(olr_region.groupby(
    'time.season').mean('time', skipna=True))

sst_region =(da.sel(lon=lon, lat=lat_range,time=time).sst)
sst_season =np.array(sst_region.groupby(
    'time.season').mean('time', skipna=True))

hadv_region =dh.sel(lon=lon, lat=lat_range,time=time).hadv
hadv_region_mean =np.array(hadv_region.mean('time', skipna=True))

#============================准备画板===================================
#========================select  不同范围里的sst===============================
jja= np.load(file="jja.npy")
djf= np.load(file="djf.npy")
mam= np.load(file="mam.npy")
son= np.load(file="son.npy")
jja[jja==0]=np.nan
djf[djf==0]=np.nan
mam[mam==0]=np.nan
son[son==0]=np.nan
#============================================================ 
fig= plt.figure(figsize=(20,15))
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
plt.rcParams['font.sans-serif']=['Fangsong']
plt.rcParams['font.size'] = 15



# # # # # #==============================draw ACT==================================
ax0=fig.add_subplot(4,1,4,projection=ccrs.PlateCarree(central_longitude =180))
cb=ax0.contourf(lon,lat_range,djf,levels=np.arange(240,275),cmap=plt.get_cmap('bwr'),    \
            transform=ccrs.PlateCarree()) 
ax0.add_feature(cfeature.NaturalEarthFeature('physical', 'land', '50m', \
                                            edgecolor='white', facecolor='white',zorder=2))
ax0.set_xticks(np.arange(-180, 210, 30),crs=ccrs.PlateCarree(central_longitude=180))
ax0.set_yticks(np.arange(-20, 20+10, 10),crs=ccrs.PlateCarree())
ax0.xaxis.set_major_formatter(LongitudeFormatter())
ax0.yaxis.set_major_formatter(LatitudeFormatter())
ax0.set_title('DJF热带海域ACT水平分布图')
ax0.set_xlabel('经度($°$)',fontsize=15)
ax0.set_ylabel('纬度($°$)',fontsize=15)
cbar = plt.colorbar(cb,shrink=0.6,ticks=[240,250,260,270],aspect=5,pad=0.01)
# contour = plt.contour(lon,lat_range, djf,5,colors='grey',zorder=1,\
#                                   transform=ccrs.PlateCarree())
#===============================================================================
ax1=fig.add_subplot(4,1,1,projection=ccrs.PlateCarree(central_longitude =180))
cb1=ax1.contourf(lon,lat_range,jja,levels=np.arange(240,275),cmap='bwr',      \
            transform=ccrs.PlateCarree()) 
ax1.add_feature(cfeature.NaturalEarthFeature('physical', 'land', '50m', \
                                            edgecolor='white', facecolor='white',zorder=2))
ax1.set_xticks(np.arange(-180, 210, 30),crs=ccrs.PlateCarree(central_longitude=180))
ax1.set_yticks(np.arange(-20, 20+10, 10),crs=ccrs.PlateCarree())
ax1.xaxis.set_major_formatter(LongitudeFormatter())
ax1.yaxis.set_major_formatter(LatitudeFormatter())
ax1.set_title('JJA热带海域ACT水平分布图')
ax1.set_xlabel('经度($°$)',fontsize=15)
ax1.set_ylabel('纬度($°$)',fontsize=15)
cbar1 = plt.colorbar(cb1,shrink=0.6,ticks=[240,250,260,270],aspect=5,pad=0.01)
# contour = plt.contour(lon,lat_range, jja,5,colors='grey',zorder=1,\
#                                   transform=ccrs.PlateCarree())
#===============================================================================
ax2=fig.add_subplot(4,1,2,projection=ccrs.PlateCarree(central_longitude =180))
cb2=ax2.contourf(lon,lat_range,mam,levels=np.arange(240,275),cmap='bwr',      \
            transform=ccrs.PlateCarree()) 
ax2.add_feature(cfeature.NaturalEarthFeature('physical', 'land', '50m', \
                                            edgecolor='white', facecolor='white',zorder=2))
ax2.set_xticks(np.arange(-180, 210, 30),crs=ccrs.PlateCarree(central_longitude=180))
ax2.set_yticks(np.arange(-20, 20+10, 10),crs=ccrs.PlateCarree())
ax2.xaxis.set_major_formatter(LongitudeFormatter())
ax2.yaxis.set_major_formatter(LatitudeFormatter())
ax2.set_title('MAM热带海域ACT水平分布图')
ax2.set_xlabel('经度($°$)',fontsize=15)
ax2.set_ylabel('纬度($°$)',fontsize=15)
cbar2 = plt.colorbar(cb2,shrink=0.6,ticks=[240,250,260,270],aspect=5,pad=0.01)
# contour = plt.contour(lon,lat_range, mam,5,colors='grey',zorder=1,\
#                                   transform=ccrs.PlateCarree())
#===============================================================================

ax3=fig.add_subplot(4,1,3,projection=ccrs.PlateCarree(central_longitude =180))
cb3=ax3.contourf(lon,lat_range,son,levels=np.arange(240,275),cmap='bwr',      \
            transform=ccrs.PlateCarree()) 
ax3.add_feature(cfeature.NaturalEarthFeature('physical', 'land', '50m', \
                                            edgecolor='white', facecolor='white',zorder=2))
ax3.set_xticks(np.arange(-180, 210, 30),crs=ccrs.PlateCarree(central_longitude=180))
ax3.set_yticks(np.arange(-20, 20+10, 10),crs=ccrs.PlateCarree())
ax3.xaxis.set_major_formatter(LongitudeFormatter())
ax3.yaxis.set_major_formatter(LatitudeFormatter())
ax3.set_title('SON热带海域ACT水平分布图')
ax3.set_xlabel('经度($°$)',fontsize=15)
ax3.set_ylabel('纬度($°$)',fontsize=15)
# contour = plt.contour(lon,lat_range, son,5,colors='grey',zorder=1,\
#                                   transform=ccrs.PlateCarree())
cbar3 = plt.colorbar(cb3,shrink=0.6,ticks=[240,250,260,270],aspect=5,pad=0.01)


fig.savefig('D:\\desktopppp\\sst_olr\\picture\\'+'不同季节态热带海域ACT水平分布图.tiff',format='tiff',dpi=150)
