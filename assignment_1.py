## Importing needed packages

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pdb
import xarray as xr

# Accessing the data
dset = xr.open_dataset(r'D:\KAUST_Course\geo_env\data\N21E039.SRTMGL1_NC.nc')

# Extracting the DEM
DEM = np.array(dset.variables['SRTMGL1_DEM'])

# Using MatPlotLib to plot and then exporting the figure as png
plt.imshow(DEM)
cbar = plt.colorbar()
cbar.set_label('Elevation (m asl)')
plt.savefig('assignment_1.png', dpi=300)

