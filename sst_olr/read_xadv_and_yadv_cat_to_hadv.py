# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 17:54:51 2021

@author: 纪
"""
from matplotlib.ticker import AutoMinorLocator, MultipleLocator
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

path0='D:\\desktopppp\\sst_olr\\interp_nan\\olr_1982_2012.nc'
da=xr.open_dataset(path0)
olr_lat=np.array(da['lat'])
olr_lon=np.array(da['lon'])
# # lat_range=olr_lat[(olr_lat>-22.5) & (olr_lat<22.5)]
olr=da.sel(lat=olr_lat,lon=olr_lon)
path1='E:\\BaiduNetdiskDownload\\MSE_budget\\xadv\\'
path2='E:\\BaiduNetdiskDownload\\MSE_budget\\yadv\\'
# path3='E:\\BaiduNetdiskDownload\\MSE_budget\\mse\\'

file_xadv=[]
file_yadv=[]
hadv_new=[]
for year in range(1982,2013):
      fn=os.path.join(path1,'xadv'+'%04.0f'%year+'.mon.161x720.nc')
      fn1=os.path.join(path2,'yadv'+'%04.0f'%year+'.mon.161x720.nc')
      file_xadv.append(fn)
      file_yadv.append(fn1)

for i in range(len(file_yadv)):
      ds=xr.open_dataset(file_xadv[i])
      ds2=xr.open_dataset(file_yadv[i])
      lon_name = 'lon'  # whatever name is in the data
      ds['_longitude_adjusted'] = xr.where(ds[lon_name] < 0, ds[lon_name]%360,\
                                          ds[lon_name])
      ds = (
        ds
        .swap_dims({lon_name: '_longitude_adjusted'})
        .sel(**{'_longitude_adjusted': sorted(ds._longitude_adjusted)})
        .drop(lon_name))
      ds = ds.rename({'_longitude_adjusted': lon_name})
# #==========================
      ds2['_longitude_adjuste'] = xr.where(ds2[lon_name] < 0, ds2[lon_name]%360,\
                                              ds2[lon_name])
      ds2 = (
        ds2
        .swap_dims({lon_name: '_longitude_adjuste'})
        .sel(**{'_longitude_adjuste': sorted(ds2._longitude_adjuste)})
        .drop(lon_name))
      ds2 = ds2.rename({'_longitude_adjuste': lon_name})
      hadv=ds.xadv+ds2.yadv
      hadv_new.append((hadv))
data=xr.concat(hadv_new,dim='time')

hadv=(data.interp(lat=da.lat.values, lon=da.lon.values))
hadv=xr.DataArray(data=hadv,dims=('time','lat','lon'),
                coords=dict(time=hadv.time,lat=hadv.lat,lon=hadv.lon))
hadv=xr.Dataset({'hadv':hadv})
hadv.to_netcdf('D:\\desktopppp\\sst_olr\\interp_nan\\hadv_interp_0826.nc')
