import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import matplotlib.colors as mcolors
from pathlib import Path

# Data path
era_path = Path("/home/desan/ESM-data/")
down_sw = era_path / 'down-short-annualcycle.nc'

data = xr.open_dataset(down_sw)
var = data['avg_sdswrf'].squeeze()

month = np.arange(1, 12.1, 1) #12 months

fz = 16

plt.figure(figsize=(20, 10))
plt.rcParams.update({'font.size': fz})
ax = plt.axes()
ax.plot(month, var,
           color='b',
           linestyle='-')
ax.set_yticks(np.arange(175, 197, 2.5))
ax.set_xticks(np.arange(1, 12.1, 1))
ax.set_xticklabels(['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'], fontsize=fz)
ax.set_ylabel("Global mean SW down" +  r" (W m$^{-2}$)", fontsize=fz)
ax.set_xlabel('Month', fontsize=fz)
ax.set_title('Mean surface downward SW radiation flux', 
                fontweight='bold')
plt.savefig('annualcycle-surf-swdown.png')
#plt.show()
