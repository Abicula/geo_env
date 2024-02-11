import tools
import matplotlib.pyplot as plt
import pandas as pd
import pdb

df_isd = tools.read_isd_csv(r'D:\KAUST_Course\geo_env\ISD_Data\41024099999.csv')

#pdb.set_trace()

plot = df_isd.plot(title='ISD data for Jeddah')
plt.savefig('ISD Jeddah.png', dpi=300)
plt.close()

######

# Calculating Relative humidity [RH] from dewpoint and air temperature
df_isd['RH'] = tools.dewpoint_to_rh(df_isd['DEW'].values, df_isd['TMP'].values)
# Calculating Heat Index
df_isd['HI'] = tools.gen_heat_index(df_isd['TMP'].values, df_isd['RH'].values)


print(df_isd.max())

print('The dates for maximum values are: ')
print(df_isd.idxmax())



print('At the date and time of the highest HI, ')
print(df_isd.loc[["2023-08-21 10:00:00"]])
print()


# Resampling to daily instead of hourly
df_isd_daily = df_isd.resample('D').mean()
print(df_isd_daily.head())
print()

############### Block for identifying heatwaves ###############
# Calculate the average maximum temperature
avg_max_temp = df_isd_daily['TMP'].rolling(window=5, min_periods=1).mean()

# Identify instances where daily maximum temperature exceeds the average by 5°C
exceedances = df_isd_daily['TMP'] > (avg_max_temp + 5)

# Find consecutive exceedances
consecutive_exceedances = exceedances.groupby((exceedances != exceedances.shift()).cumsum()).cumcount() + 1

# Filter for instances where consecutive exceedances are more than 5 days
instances = consecutive_exceedances >= 5

# Print instances where the condition is met
print("Instances where daily maximum temperature exceeds average by 5°C for more than five consecutive days:")
print(df_isd_daily[instances])
###############################################################


HI_timeseries = plt.plot(df_isd_daily.index, df_isd_daily['HI'])
plt.title('Daily averages of HI in Jeddah')
plt.xlabel('Date')
plt.ylabel('Heat Index (HI)')
plt.savefig('Daily averages of HI', dpi=300)
plt.close()


df_isd_alt = df_isd
df_isd_alt['TMP'] = df_isd_alt['TMP'] + 3
df_isd_alt['HI1'] = tools.gen_heat_index(df_isd_alt['TMP'].values, df_isd['RH'].values)
print('Maximum HI after additional warming = ', df_isd_alt['HI1'].max())