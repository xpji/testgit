# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 12:55:21 2021

@author: 纪
"""
import xarray as xr
import netCDF4 as nc
path1='D:\\desktopppp\\sst_olr\\olr.mon.mean.nc'
da=xr.open_dataset(path1)
path2='D:\\desktopppp\\sst_olr\\sst.mnmean.nc'

ds=xr.open_dataset(path2)

sst= ds.interp(lat=da.lat.values, lon=da.lon.values)

time0=da['time'][:]

time0=time0.loc['1982':'2012'][:]

time=sst['time'][:]

time=time.loc['1982':'2012'][:]

sst_1982_2012=sst.sel(time=time)

olr_1982_2012=da.sel(time=time0)

sst_1982_2012.to_netcdf('D:\\desktopppp\\sst_olr\\interp_nan\\sst_interp_1982_2012.nc')

olr_1982_2012.to_netcdf('D:\\desktopppp\\sst_olr\\interp_nan\\olr_1982_2012.nc')

lat=sst['lat'][:]

lat_range = lat[(lat>-22.5) & (lat<22.5)]

sst_region =sst.sel(lat=lat_range,time=time)

sst_region.to_netcdf('D:\\desktopppp\\sst_olr\\interp_nan\\sst_interp_region.nc')

