# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 23:11:09 2021

@author: 纪
"""
import xarray as xr
import numpy as np
from xarray.backends import NetCDF4DataStore
import salem
from datetime import datetime
from siphon.catalog import TDSCatalog
import cartopy.crs as ccrs
import cartopy.feature as cfeat
from cartopy.mpl.ticker import LongitudeFormatter,LatitudeFormatter
from cartopy.io.shapereader import Reader, natural_earth
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import geopandas

shp_path = './ne_10m_ocean_scale_rank/'
shp = geopandas.read_file(shp_path + 'ne_10m_ocean_scale_rank.shp')
t = temp.salem.roi(shape=shp)
t.plot.contourf(
    ax=create_map(), 
    cmap='Spectral_r', 
    levels=levels, 
    cbar_kwargs=cbar_kwargs, 
    transform=ccrs.PlateCarree()
)