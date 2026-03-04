import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import matplotlib.colors as mcolors
from pathlib import Path

# Data path
era_path = Path("/home/desan/ESM-data/")
top_net_sw = era_path / 'net-short-annual-Zonmean.nc'
top_net_lw = era_path / 'net-long-annual-Zonmean.nc'

cases = (top_net_sw, top_net_lw)
varc = ('avg_tnswrf', 'avg_tnlwrf')

n=0
var = [  ]
for i in cases:
    data = xr.open_dataset(i)
    dat = data[varc[n]].squeeze()
    var.append(dat)
    n = n+1

lat = np.arange(-90.0, 90.25, 0.25) #721

fz = 12

fig, ax = plt.subplots(2)
#fig.tight_layout()
ax[0].plot(lat, var[0],
           color='b',
           linestyle='-')
ax[0].plot(lat, -1.0*var[1],
           color='r',
           linestyle='--')
ax[0].set_xlabel("Latitude", fontsize=fz)
ax[0].set_ylabel("Radiation" +  r" (W m$^{-2}$)", fontsize=fz)
ax[0].set_yticks(np.arange(30,330.1,30))
ax[0].set_xticks(np.arange(-90, 90.1, 30))
ax[0].set_xticklabels(['90S','60S','30S','EQ','30N','60N','90N'], fontsize=fz)
ax[0].set_xlim(-90, 90)
ax[0].set_ylim(30,330)
ax[0].set_xlabel('Latitude', fontsize=fz)
ax[0].legend(['Absorbed solar radiation','Outgoing longwave radiation'],
             edgecolor='white')
ax[0].set_title('Radiation zonal mean at the TOA in annual mean',
                fontweight='bold')

ax[1].plot(lat, var[0]- (-1.0*var[1]),
           color='g',
           linestyle='-')
ax[1].set_yticks(np.arange(-140, 80, 20))
ax[1].set_xticks(np.arange(-90, 90.1, 30))
ax[1].set_xticklabels(['90S','60S','30S','EQ','30N','60N','90N'], fontsize=fz)
ax[1].set_xlim(-90, 90)
ax[1].set_ylabel("Radiation" +  r" (W m$^{-2}$)", fontsize=fz)
ax[1].set_xlabel('Latitude', fontsize=fz)
ax[1].set_title('Absorbed solar radiation - Outgoing longwave radiation', 
                fontweight='bold')
plt.subplots_adjust(hspace=0.5)
plt.savefig('rad-zonalmean.png')
#plt.show()
