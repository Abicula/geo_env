## Importing needed packages

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pdb
import xarray as xr
import tools

# Accessing the data
dset = xr.open_dataset(r'D:\KAUST_Course\geo_env\ERA5_Data\download.nc')


############# Extracting relevant variables #####################

t2m = np.array(dset.variables['t2m'])
tp = np.array(dset.variables['tp'])
latitude = np.array(dset.variables['latitude'])
longitude = np.array(dset.variables['longitude'])
time_dt = np.array(dset.variables['time'])

################################################################

############# Converting temperature from K to C and precipitation from m/h to mm/h #############

t2m = t2m - 273.15
tp = tp * 1000


if t2m.ndim == 4:
    t2m = np.nanmean(t2m, axis=1)
    tp = np.nanmean(tp, axis=1)
    
#################################################################################################

################# Creating pandas df localized near the reservoir #################

df_era5 = pd.DataFrame(index=time_dt)
df_era5['t2m'] = t2m[:,3,2]
df_era5['tp'] = tp[:,3,2]

###################################################################################

################# Plotting the time series #################

df_era5.plot()
plt.savefig('time series for t2m & tp.png', dpi=300)
plt.close()

############################################################

################# Resamplig precipitation to annual #################

annual_prec = df_era5['tp'].resample('YE').mean()*24*365.25
mean_annual_prec = np.nanmean(annual_prec)
print('The mean annual prec = ', mean_annual_prec)
print()

#####################################################################

################# Calculating PE #################

tmin = df_era5['t2m'].resample('D').min().values
tmax = df_era5['t2m'].resample('D').max().values
tmean = df_era5['t2m'].resample('D').mean().values
doy = df_era5['t2m'].resample('D').mean().index.dayofyear
lat = 21.25

# Computing PE

pe = tools.hargreaves_samani_1982(tmin, tmax, tmean, lat, doy)

# Calculating yearly avg
remainder = 365 - (len(pe) % 365)
days_per_year = 365
total_days = len(pe)
padding = days_per_year - (total_days % days_per_year)
padded_values = np.append(pe, np.zeros(padding))
pe_yearly_data = padded_values.reshape(-1, days_per_year)
yearly_average = np.mean(pe_yearly_data, axis=1) * 365    # to convert from mm/day to mm/year
mean_over_years = np.mean(yearly_average)
print('The yearly pe avg = ', mean_over_years)
###################################################
pdb.set_trace()

################# Plotting PE timeseries #################

ts_index = df_era5['t2m'].resample('D').mean().index
plt.figure()
plt.plot(ts_index, pe, label='Potential Evaporation')
plt.xlabel('Time')
plt.ylabel('Potential evaporation (mm/d)')
plt.savefig('PE.png', dpi=300)
plt.close



##############################################################################################################################################################
##############################################################################################################################################################
################# The bottom section is an attempt using previous instructions (which has been commented out, but kept for future reference) #################
##############################################################################################################################################################
##############################################################################################################################################################


# ########### Locating Wadi Murwani reservoir #############

# lat = 22.00
# lon = 39.55

# selected_location = dset.sel(latitude=lat, longitude=lon, method='nearest')

# ###########################################################

# ################### Plotting ##########################

# fig, ax1 = plt.subplots()

# ax1.plot(selected_location['time'], selected_location['t2m'], label='T [°C]', color='tab:blue')
# ax1.set_xlabel('Time')
# ax1.set_ylabel('Temperature [°C]', color='tab:blue')
# ax1.tick_params(axis='y', labelcolor='tab:blue')

# ax2 = ax1.twinx()
# ax2.plot(selected_location['time'], selected_location['tp'], label='P [mm]', color='tab:orange')
# ax2.set_ylabel('Precipitation [mm]', color='tab:orange')
# ax2.tick_params(axis='y', labelcolor='tab:orange')

# plt.title('Temperature and Precipitation Time Series at Wadi Murwani Reservoir')
# fig.tight_layout()
# plt.savefig('T&Prec_at_Murwani.png', dpi=300)
# plt.close()

# #######################################################


# ############### Avg annual precipitation ###############
# # Resampling to daily instead of hourly
# annual_prec = dset['tp'].resample(time='A').mean()
# print('[+]Avg annual prec = ', annual_prec.head())
# print()

# ########################################################


# ############### Potential temperature calc ###############
# # Extracting daily min, max, and avg from dset
# tmin = dset['t2m'].resample(time='D').min().values
# tmax = dset['t2m'].resample(time='D').max().values
# tmean = dset['t2m'].resample(time='D').mean().values
# doy = (dset['t2m'].resample(time='D').mean().time).dt.dayofyear.values
# # Using function in tools
# pe = tools.hargreaves_samani_1982(tmin, tmax, tmean, lat, doy)

# ##########################################################
# #pdb.set_trace()
# ################### Plotting ##########################
# pe_adj = pe[:, 0, 0, 0]
# time_index = np.arange(1, 2184, 1)
# plt.figure(figsize=(10, 6), tight_layout=True)
# plt.plot(time_index, pe_adj, label='Potential Evaporation')
# plt.xlabel('Day')
# plt.ylabel('PE [mm/day]')
# plt.title('Potential Evaporation Time Series')
# plt.grid(True)
# plt.savefig('PE.png', dpi=300)
# plt.close()

# #######################################################

# ############### Potential evaporation mean annual ###############
# # Extracting daily min, max, and avg from dset
# # Convert pe_adj to a pandas Series
# pe_series = pd.Series(pe_adj, index=time_index)

# # Resample to annual frequency and calculate mean
# # Since the index is numerical, you can't use resample directly
# # Instead, you can group by year and calculate the mean
# annual_mean_pe = pe_series.groupby((time_index - 1) // 365).mean()

# # Calculate the mean of the annual means
# mean_annual_pe = annual_mean_pe.mean()

# print('[+] annual mean pe = ', annual_mean_pe)
# print()
# print('[+] mean annual pe = ', mean_annual_pe) 

# ##########################################################