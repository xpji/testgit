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
olr_region =ds.sel(lon=lon, lat=lat_range,time=time)

season_summary = olr_region.time.dt.month.isin([6,7,8])

data=olr_region.olr.loc[season_summary]
#