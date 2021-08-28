# -*- coding: utf-8 -*-
"""
Created on Wed Aug 11 11:17:43 2021

@author: 纪
"""


from sklearn.linear_model import LinearRegression 

import cartopy.crs as ccrs
import pandas as pd
import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt


path1='D:\\desktopppp\\olr_mean.csv'
path2='D:\\desktopppp\\diff.csv'
da=pd.read_csv(path1)
ds=pd.read_csv(path2)
#==================
dif0=ds['0diff']
sst=np.arange(20,32,0.25)
#=======================最小二乘法==========================================
x1=sst[21:36]
y1=np.array(dif0[21:36])
x2=sst[35:39]
y2=dif0[35:39]
# A = np.vstack([x1, np.ones(len(x1))]).T
# m1, c1 = np.linalg.lstsq(A, dif0[21:36], rcond=None)[0]
# A2 = np.vstack([x2, np.ones(len(x2))]).T
# m2, c2 = np.linalg.lstsq(A2, dif0[35:39], rcond=None)[0]
x=x1.reshape((-1, 1))
y=y1.reshape((-1, 1))
reg = LinearRegression().fit(x, y)
m=reg.coef_[0][0]
c=reg.intercept_[0]
r=reg.score(x, y)
print("一元回归方程为:  Y = %.5fX + (%.5f)" % (reg.coef_[0][0], reg.intercept_[0]))
print("R平方为: %s" % reg.score(x, y))
#==========================================================================
xx=sst[35:39]
yy=np.array(dif0[35:39])
x_2=xx.reshape((-1, 1))
y_2=yy.reshape((-1, 1))
reg2 = LinearRegression().fit(x_2, y_2)
m2=reg2.coef_[0][0]
c2=reg2.intercept_[0]
r2=reg2.score(x_2, y_2)
print("一元回归方程为:  Y = %.5fX + (%.5f)" % (reg2.coef_[0][0], reg2.intercept_[0]))
print("R平方为: %s" % reg2.score(x_2, y_2))
#==========================================================================
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
fig=plt.figure(figsize=(10,6))
ax=fig.add_subplot(111)
ax.invert_yaxis()
ax.tick_params( axis='x',direction='in',labelsize=15)
ax.tick_params(axis='y',direction='in',labelsize=15)

ax.plot(sst,dif0,'b',label='$\partial $OLR/$\partial $SST')

ax.set_xlim(20,31)
ax.set_xticks(np.linspace(20, 31, 12))
ax.set_ylim(10,-20)#末尾不显示210，280
ax.set_yticks(np.linspace(10, -20, 6))
ax.set_title(' $\partial $OLR/$\partial $SST and EOT',fontsize=20)
ax.set_ylabel('Changing rate(w/m$^2$/°C)',fontsize=20)
ax.set_xlabel('SST($°$C)',fontsize=20)
plt.axhline(y=0,linestyle='-',color='k',xmin=0,xmax=0.471,linewidth=2)
plt.axhline(y=0,linestyle='-',color='k',xmin=0.865,xmax=1,linewidth=2)

plt.axvline(x=29.475,linestyle='--',color='deepskyblue')
plt.axvline(x=25.25,linestyle='--',color='deepskyblue')

# plt.axvline(x=28.75,linestyle='--',color='deepskyblue')
ax.plot(sst[21:39],dif0[21:39],'k',linewidth=3,label='EOT',alpha=0.8)
#nihequxian
ax.plot(x, m*x + c, 'r', linewidth=3)
ax.plot(xx, m2*xx + c2,'gold',linewidth=3)
ax.legend()
# fig.savefig('D:\\desktopppp\\sst_olr\\picture\\'+'EOT_LSTSQ_olr_sst.tiff',format='tiff',dpi=150)





















