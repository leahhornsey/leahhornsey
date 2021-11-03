#!/usr/bin/env python
# coding: utf-8

# In[121]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import xarray as xr
# if you get errors to import these packages , you will need to install them in Anaconda
# in anaconda command prompt (windows) or terminal (mac/linux) 
# Activate your environment, then type:
# conda install xarray


# In[122]:


## load Moab, Utah temperature data
# load excel data as pandas dataframe
df=pd.read_excel(r'C:\Users\Lenovo\Documents\QuantitativeTechniques\MOAB_1893_2020_MeanMonthlyTemp.xlsx')
data=df.to_numpy()
TMP_MOAB_JUL = data[:,7]
TMP_MOAB_JUL
#years = data[0:,0]

# first replace the missing data ("None") with np.nan
missing_index= (TMP_MOAB_JUL == -999) # first identify the missing data
TMP_MOAB_JUL[missing_index] = np.nan
TMP_MOAB_JUL_degC=(TMP_MOAB_JUL-32)*(5/9)
TMP_MOAB_JUL_degC

#TMP_MOAB_year=np.nanmean(TMP_MOAB_month,1)
# unit conversion deg F ->deg C
#TMP_MOAB_year_degC=(TMP_MOAB_year-32)*(5/9)
#year=df.Year.to_numpy()
#TMP_MOAB_year_degC


# In[123]:


# Download the most recent NCEP renalysis monthly data from the link below:
# https://psl.noaa.gov/data/gridded/data.ncep.reanalysis.derived.surface.html
# read NCEP reanalysis monthly data (in netcdf format)
# if you get an error in this step, most likely the netcdf4 package is missing in your environment
# to install netcdf4 package, type "conda install netcdf4" in command line
ds=xr.open_dataset('./air.mon.mean.nc')
# show a summary of the dataset
ds


# In[124]:


# extract surface air temperature data for 1893 to 2020
TMP_NCEP=ds.air.sel(time=slice("1948-01-01","2020-12-31"))


# In[125]:


# Moab, Utah lat lon
# 38.5733° N, 109.5498° W
# note that the longitude range in NCEP data is 0 - 360 deg

# select data for the grid cell Moab located
TMP_MOAB_NCEP=TMP_NCEP.sel(lat=38.5733,lon=360-109.5498,method="nearest")

# calculate annual mean temperature for Moab
TMP_MOAB_NCEP_year=TMP_MOAB_NCEP.groupby('time.year').mean('time')

# calculate climatological mean temperature for MOAB
TMP_MOAB_NCEP_month=TMP_MOAB_NCEP.groupby('time.month').mean('time')

# July temperature for Moab
mon=7;
TMP_MOAB_NCEP_JUL=TMP_MOAB_NCEP.sel(time=TMP_MOAB_NCEP['time.month']==mon)
TMP_MOAB_NCEP_JUL


# In[126]:


## make a figure that fits into a single column
fig=plt.figure(figsize=(3.5, 2.5)) # define figure size, unit: inches
ax=fig.add_axes([0.1, 0.15, 0.8, 0.8])
cmap=plt.get_cmap('Paired')
plt.plot(year,TMP_MOAB_JUL_degC,label='Measured (Moab site)',color=cmap(0)) 
plt.plot(TMP_MOAB_NCEP_year.year,TMP_MOAB_NCEP_JUL,label='NCEP (regional)',color=cmap(1))
plt.xlabel('Year')
plt.ylabel('Annual mean T ($^\circ$C)')
## add figure legend
plt.legend()

## save figure as .PDF and .PNG
## put save commands before plt.show()
fn='Fig_MOAB_temp'
plt.savefig('./fig/' +fn+ '.pdf',bbox_inches="tight")
plt.savefig('./fig/'+fn+'.png',bbox_inches="tight")
plt.show()


# In[127]:


import matplotlib.path as mpath
import xarray as xr
import cartopy.crs as ccrs

# if you get errors to import these packages , you will need to install them in Anaconda
# in anaconda command prompt (windows) or terminal (mac/linux) 
# Activate your environment, then type:
# conda install cartopy xarray


# In[128]:


ds=xr.open_dataset('./air.mon.mean.nc')

# extract surface air temperature data for 1948 to 2020
TMP_NCEP1=ds.air.sel(time=slice("1950-01-01","1960-12-01"))
TMP_NCEP2=ds.air.sel(time=slice("2010-01-01","2020-12-01"))

# Select JULY data for every year and average
TMP_NCEP_JUL1=TMP_NCEP1.sel(time=TMP_NCEP1['time.month']==7).mean(dim='time')
TMP_NCEP_JUL2=TMP_NCEP2.sel(time=TMP_NCEP2['time.month']==7).mean(dim='time')

# X=np.append(TMP_NCEP_mean.lon.values,360)
# Y=np.append(TMP_NCEP_mean.lat.values,-90)
X=ds.lon.values
Y=ds.lat.values

# grid boundaries
Xb=np.arange(-2.5/2, 360,2.5)
Yb=np.arange(90-2.5/2, -90,-2.5)
Yb=np.append(90,Yb)
Yb=np.append(Yb,-90)


# In[129]:


fig=plt.figure(figsize=(8, 5))
ax11 = fig.add_axes([0.42, 0.7,0.3,0.25],projection=ccrs.PlateCarree(central_longitude=-150))
ax11.coastlines()
cf=ax11.pcolormesh(Xb,Yb,TMP_NCEP_JUL1.values, transform=ccrs.PlateCarree(),vmin=-75,vmax=45,cmap='plasma',rasterized=True)
ax11.set_title('July, 1950-1960')
###
####
ax21 = fig.add_axes([0.42, 0.4,0.3,0.25],projection=ccrs.PlateCarree(central_longitude=-150))
ax21.coastlines()
cf=ax21.pcolormesh(Xb,Yb,TMP_NCEP_JUL2.values, transform=ccrs.PlateCarree(),vmin=-75,vmax=45,cmap='plasma',rasterized=True)
ax21.set_title('July, 2010-2020')

# add color bar
ax_cb = fig.add_axes([0.73, 0.41,0.0125,0.53])
fig.colorbar(cf, cax=ax_cb, label='T ($^\circ$C)')

#calculate difference
delta_TMP_JUL=TMP_NCEP_JUL2-TMP_NCEP_JUL1

ax12 = fig.add_axes([0.42, 0.1,0.3,0.25],projection=ccrs.PlateCarree(central_longitude=-150))
ax12.coastlines()
cf=ax12.pcolormesh(Xb,Yb,delta_TMP_JUL.values, transform=ccrs.PlateCarree(),vmin=-15,vmax=15,cmap='RdBu_r',rasterized=True)
ax12.set_title('July, Difference')

ax_cb2 = fig.add_axes([0.73, 0.1,0.0125,0.25])
fig.colorbar(cf, cax=ax_cb2, label='$\Delta$T ($^\circ$C)')

fn='Fig_Jan_July_temp_diff_rasterized'
plt.savefig('./fig/'+fn+'.pdf',bbox_inches="tight",dpi=300)
plt.savefig('./fig/'+fn+'.png',bbox_inches="tight",dpi=300)

plt.show()


# In[ ]:





# In[ ]:




