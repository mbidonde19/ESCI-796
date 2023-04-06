# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 14:43:26 2023

@author: mbido
"""
# Load in libraries
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
#%% Load in HAB data
# Load in the HAB data
dfhab = pd.read_csv('HAB data.csv', parse_dates=['Year'], index_col='Year')

#%% Load in discharge file
# Drainage area flowing into gauge point
drainage = 1342

# Load in the file, set Date as index
dfdis = pd.read_csv('Littlefalls.txt', comment = "#", delimiter='\t', header = 1,
                     parse_dates=['20d'], index_col=['20d'])

# Drop unused columns
dfdis.drop(columns = {"5s", "15s", "10s"}, inplace = True)

# Fill in missing values
dfdis.interpolate(method = 'linear')

# Convert the discharge value
dfdis["Discharge_mm"] = (dfdis["14n"]/drainage) * 26334720   #to mm/day

# Drop old column
dfdis.drop(columns = {"14n"}, inplace = True)

#%% Load in precip file
#Load in the file
dfp = pd.read_csv('3263069.csv', parse_dates=['DATE'], index_col=['DATE'])

# Fill missing values with 0
dfp = dfp.fillna(0)

# See if MDPR data exists
if 'MDPR' in dfp.columns.tolist():
     dfp['Combined'] = dfp['MDPR'] + dfp['PRCP']
else:
    dfp['Combined'] = dfp['PRCP']

#Convert to mm
dfp["Combined_Precip_mm"] = dfp["Combined"] * 25.4

#Delete old dataframes
dfp = dfp[['Combined_Precip_mm']]

#%% Initial Plots

fig1, ax1 = plt.subplots()
ax1.bar(dfhab.index, dfhab['Number of Weeks on DEC Notification List'], label = 'Weeks on DEC List')

fig2, ax2 = plt.subplots()
ax2.bar(dfdis.index, dfdis['Discharge_mm'], label = 'Discharge (mm)')
ax2.set_title('Discharge')

fig3, ax3 = plt.subplots()
ax3.bar(dfp.index, dfp['Combined_Precip_mm'], label = 'Precip (mm)',)
ax3.set_title('Combined Precipitation')




#%% Perform Calculations
dfyear = dfdis['Discharge_mm'].resample('Y').mean()

dfyear['Combined_Precip_mm'] = dfp['Combined_Precip_mm'].resample('Y').mean()


#%% Look at different Lakes

dflake = dfhab.sort_values('Waterbody Name', dfhab.index)












