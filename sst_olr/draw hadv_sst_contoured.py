# -*- coding: utf-8 -*-
"""
Created on Wed Aug 11 21:50:03 2021

@author: 纪
"""
from cartopy.util import add_cyclic_point
import seaborn as sns
from matplotlib.ticker import AutoMinorLocator, MultipleLocator
import xarray as xr
import netCDF4 as nc
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
path='D:\\desktopppp\\sst_olr\\interp_nan\\sst_interp_1982_2012.nc'
ds=xr.open_dataset(path)
path1='D:\\desktopppp\\sst_olr\\interp_nan\\olr_1982_2012.nc'
da=xr.open_dataset(path1)
path2='D:\\desktopppp\\sst_olr\\interp_nan\\hadv_interp.nc'
hadv=xr.open_dataset(path2)
#select range that you need
lat=ds['lat']
lon=np.array(ds['lon'])
lat_range= lat[(lat>-22.5) & (lat<22.5)]
lon_range=lon[(lon>=120)&(lon<=260)]
sst=ds.sel(lat=lat_range)['sst']
olr=da.sel(lat=lat_range)['olr']
hadv=hadv.sel(lat=lat_range)['hadv']
x=np.arange(20,32.5,0.5)
x1=np.arange(-25,25,5)
sst_select=[]
olr_select=[]

for i in x:
    idx=(sst>=i)&(sst<=i+0.5)
    sst_select.append(np.array(sst)[idx])
    olr_select.append(np.array(olr)[idx])
    olr_mean=[]
    for j in range(len(olr_select)):
        olr_mean.append(np.nanmean(olr_select[j]))
olr_select2=[]
hadv_select=[]
for k in x1:
    idx2=(hadv>=k)&(hadv<=k+5)
    hadv_select.append(np.array(hadv)[idx2])
    olr_select2.append(np.array(olr)[idx2])
    olr_mean2=[]
    for m in range(len(olr_select2)):
        olr_mean2.append(np.nanmean(olr_select2[m]))
# X,Y = np.meshgrid(x1,x)

# fig=plt.figure()
# ax=fig.add_subplot()

# ax.scatter(olr_mean,olr_mean2)
# contour = ax.contour(x1,x, Y,colors='k')
# ax.set_xlim(-200,200)
