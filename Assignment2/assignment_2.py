# Imports

#################
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pdb
import xarray as xr
#################

# Data exploration
#################
dset = xr.open_dataset(r'D:\KAUST_Course\geo_env\Climate_Model_Data\tas_Amon_GFDL-ESM4_historical_r1i1p1f1_gr1_195001-201412.nc')

#pdb.set_trace()

dset.close()
#################


# Opening 1850-1900 dataset
#################
dset = xr.open_dataset(r'D:\KAUST_Course\geo_env\Climate_Model_Data\tas_Amon_GFDL-ESM4_historical_r1i1p1f1_gr1_185001-194912.nc')

mean_pre_ind = np.mean(dset['tas'].sel(time=slice('18500101', '19001231')), axis=0)

dset.close()
#################


# Calculate for other climate scenarios
#################
dset = xr.open_dataset(r'D:\KAUST_Course\geo_env\Climate_Model_Data\tas_Amon_GFDL-ESM4_ssp119_r1i1p1f1_gr1_201501-210012.nc')

mean_ssp119 = np.mean(dset['tas'].sel(time=slice('20710101', '21001231')), axis=0)

dset.close()

##

dset = xr.open_dataset(r'D:\KAUST_Course\geo_env\Climate_Model_Data\tas_Amon_GFDL-ESM4_ssp245_r1i1p1f1_gr1_201501-210012.nc')

mean_ssp245 = np.mean(dset['tas'].sel(time=slice('20710101', '21001231')), axis=0)

dset.close()

##

dset = xr.open_dataset(r'D:\KAUST_Course\geo_env\Climate_Model_Data\tas_Amon_GFDL-ESM4_ssp585_r1i1p1f1_gr1_201501-210012.nc')

mean_ssp585 = np.mean(dset['tas'].sel(time=slice('20710101', '21001231')), axis=0)

dset.close()
#################


# Finding the difference
#################
diff_pre_ind_ssp119 = mean_ssp119 - mean_pre_ind

diff_pre_ind_ssp245 = mean_ssp245 - mean_pre_ind

diff_pre_ind_ssp585 = mean_ssp585 - mean_pre_ind
#################


# Visualization of difference mean temperatures
#################
ssp119 = plt.imshow(diff_pre_ind_ssp119, cmap='coolwarm', origin='lower', vmin=-1*np.nanmax(diff_pre_ind_ssp119), vmax=np.nanmax(diff_pre_ind_ssp119))
colorbar119 = plt.colorbar(ssp119)
colorbar119.set_label('Temperature (K)')
plt.title('Difference between pre industrial temp and SSP119')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')

#plt.show
plt.savefig('pre vs SSP119.png', dpi=300)
plt.close()

##

ssp245 = plt.imshow(diff_pre_ind_ssp245, cmap='coolwarm', origin='lower', vmin=np.nanmax(diff_pre_ind_ssp245)*-1, vmax=np.nanmax(diff_pre_ind_ssp245))
colorbar245 = plt.colorbar(ssp245)
colorbar245.set_label('Temperature (K)')
plt.title('Difference between pre industrial temp and SSP245')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')

#plt.show
plt.savefig('pre vs SSP245.png', dpi=300)
plt.close()

##

ssp585 = plt.imshow(diff_pre_ind_ssp585, cmap='coolwarm', origin='lower', vmin=np.nanmax(diff_pre_ind_ssp585)*-1, vmax=np.nanmax(diff_pre_ind_ssp585))
colorbar585 = plt.colorbar(ssp585)
colorbar585.set_label('Temperature (K)')
plt.title('Difference between pre industrial temp and SSP585')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')

#plt.show
plt.savefig('pre vs SSP585.png', dpi=300)
plt.close()
#################