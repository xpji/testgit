
import statistics

from matplotlib.ticker import AutoMinorLocator
from scipy.optimize import curve_fit
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
from scipy.optimize import leastsq
from itertools import groupby
from scipy import signal
import xarray as xr
import netCDF4 as nc
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#read nc file
path='D:\\desktopppp\\sst_olr\\interp_nan\\sst_interp_1982_2012.nc'
ds=xr.open_dataset(path)
path1='D:\\desktopppp\\sst_olr\\interp_nan\\olr_1982_2012.nc'
da=xr.open_dataset(path1)
#select range that you need
lat=ds['lat']
lon=np.array(ds['lon'])

lat_range= lat[(lat>-22.5) & (lat<22.5)]
lon_range=lon[(lon>=120)&(lon<=260)]
sst=ds.sel(lat=lat_range,lon=lon_range)
olr=da.sel(lat=lat_range,lon=lon_range)
#将数据按照年进行平均处理
# olr_summary = olr.groupby('time.day').mean('time', skipna=True)
# summary1=summary.olr.mean(dim='year')
# sst_summary = sst.groupby('time.day').mean('time', skipna=True)
#select the first year_mean data 既1982年的年平均数据
sst_1982=np.array(sst.sst)
olr_1982=np.array(olr.olr)
#select 以0.25°C为一个bins 落入该区间内的数据进行分组,并统计个数
sst_range=np.arange(20,32,0.25)
num=[]
sst_bin=[]
olr_bin=[]
# 做一个循环处理
for i in sst_range:
    
    idx=(sst_1982>=i)&(sst_1982<=i+0.25) #bool索引，true or false
    sst_bin.append(sst_1982[idx])
    olr_bin.append(olr_1982[idx])
    ol=olr_1982[idx]
    num.append(len(ol))
    

#对于每一个区间里的olr数据进行求mean std     
olr_mean=[]
sst_mean=[]
olr_std=[]

    
for  j in range(len(olr_bin)):
    
    olr_mean.append(np.mean(olr_bin[j]))
    
for  i in range(len(sst_bin)):
     
    sst_mean.append(np.array(np.mean(sst_bin[i])))
olr_mean0=np.array(olr_mean    )
olr_bin0=np.array(olr_bin)
sst_bin0=np.array(sst_bin)
o2=[]
olr_std=[]
for i in range(len(olr_bin0)):
     o2.append(np.array((olr_bin0[i]-olr_mean0[i])*(olr_bin0[i]-olr_mean0[i])))
for i in range(len(o2)):
     olr_std.append(sum(o2[i])/len(olr_bin0[i]))
     
olr_std=np.array(np.sqrt(olr_std))
     

olr_mean=np.array(olr_mean)
sst_mean=np.array(sst_mean)
sst_bin=np.array(sst_bin)
#===============================计算 olr随sst的变化率====================
diff=np.gradient(olr_mean)    

y1=olr_mean+olr_std
y2=olr_mean-olr_std

    
num10=np.log10(num)   
 #=================================plot======================================
x=sst_range
y=olr_mean
fig=plt.figure(figsize=(8,16))
ax = fig.add_subplot(2,1,1)
ax3 = fig.add_subplot(2,1,2)
# ax4=fig.add_subplot(113)
# fig.tight_layout() 
plt.tick_params(labelsize=15)
# ax=fig.add_subplot(2,1,1)
#散点图
ax.scatter(sst_1982,olr_1982,s=1)
ax.invert_yaxis()
ax.set_ylim(320,160)
ax.set_xlim(20,32)
# ax.grid(color='w')
x_grid=ax.get_xgridlines()
x_grid[3].set_color('k')  
ax.plot(x,y,'r',linewidth=3)    #
ax.set_xlabel('SST(°C)',fontsize=15)
ax.spines['left'].set_color ('r')#设置轴的颜色
ax.tick_params( axis='y',direction='out', colors='red',
              labelcolor='r',   labelsize=10)#设置y轴颜色，外凸间隔，字体大小
ax.tick_params( axis='x',direction='out',
            )
ax.tick_params(axis='y',colors='r')
ax.set_xticks(np.linspace(20, 32, 7))
ax.set_yticks(range(160, 360, 40))#设置y轴显示范围以及间隔
ax.set_ylabel('OLR(w/m$^2$)',fontsize=15,color='r')

ax.tick_params(axis='y',which='minor', length=5,color='r')
ax.tick_params(which='major', width=1.0,length=10)
ax.yaxis.set_minor_locator(AutoMinorLocator(2))
ax.xaxis.set_minor_locator(AutoMinorLocator(2))
ax.set_title('SST and OLR',fontsize=20)

# ax.plot(x, y1, x, y2, color='r')
ax.fill_between(x, y1, y2,alpha=0.3,facecolor='r', where=y2 >= y1,  interpolate=True)
ax.fill_between(x, y1, y2, alpha=0.3,facecolor='r',where=y2 <= y1,  interpolate=True)
                
# #共用x轴，再画一个y

ax2 = ax.twinx()
ax2.tick_params( axis='y',direction='out',
          labelsize=15)#设置y轴颜色，外凸间隔，字体大小
ax2.spines['left'].set_color ('r')
ax2.plot(x,num10,'k')
ax2.set_ylim(1,5)
ax2.set_ylabel('log$_1$$_0$(Numbers)',fontsize=15)
ax2.yaxis.set_minor_locator(AutoMinorLocator(2))
ax2.tick_params(which='minor', length=5)
ax2.tick_params(which='major', width=1.0,length=10)
ax2.tick_params(direction='out', axis='y',
          labelsize=15, grid_alpha=0.5)     
ax2.set_yticks(range(1, 6, 1)) 

#draw     olr_sst change_rate plot=======================
ax3.plot(x,diff,'b')
ax3.invert_yaxis()
ax3.set_xlim(20,32)

ax3.grid(linestyle='--')
ax3.grid(linestyle='--',which='minor',axis='x',alpha=0.75)
ax3.xaxis.set_minor_locator(AutoMinorLocator(2))
ax3.yaxis.set_minor_locator(AutoMinorLocator(2))
ax3.tick_params(axis='y',which='minor', length=5)
ax3.tick_params(axis='y',which='major', length=10)
ax3.tick_params(axis='x',which='minor', length=5)
ax3.tick_params(axis='x',which='major', length=10)
ax3.set_xlabel('SST(°C)',fontsize=15)
ax3.set_ylabel('Changing rate(w/m$^2$/°C)',fontsize=15)
ax3.set_title(' $\partial $OLR/$\partial $SST',fontsize=20)


    
# ###############=ax4
