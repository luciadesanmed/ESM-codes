import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import matplotlib.colors as mcolors
from pathlib import Path

# Data path
era_path = Path("/home/desan/ESM-data/")
net_lw = era_path / 'surface-net-lw.nc'
net_sw = era_path / 'surface-net-sw.nc'
net_sh = era_path / 'surface-sensible-heat.nc'
net_lh = era_path / 'surface-latent-heat.nc'

cases = (net_lw, net_sw, net_sh, net_lh)
varc = ('avg_snlwrf', 'avg_snswrf', 'avg_ishf', 'avg_slhtf')

latmin =  21.5139417 #21°30'50.19"N
latmax =  22.4147556 #22°24'53.12"N
lonmin = 257.052264 #102°56'51.85"O
lonmax = 258.204600 #101°47'43.44"O

n=0
var = [  ]
#for i in cases:
data = xr.open_dataset(cases[0])
dat = data[varc[0]].squeeze()
#Chop for my area:
dat_sub = dat.sel(latitude=slice(latmax, latmin), longitude=slice(lonmin, lonmax))

    #var.append(dat)
    #n = n+1

#lat = np.arange(-90.0, 90.25, 0.25) #721

#fz = 12

#fig, ax = plt.subplots(2)
#fig.tight_layout()
#ax[0].plot(lat, var[0],
#           color='b',
#           linestyle='-')
#ax[0].plot(lat, -1.0*var[1],
#           color='r',
#           linestyle='--')
#ax[0].set_xlabel("Latitude", fontsize=fz)
#ax[0].set_ylabel("Radiation" +  r" (W m$^{-2}$)", fontsize=fz)
#ax[0].set_yticks(np.arange(30,330.1,30))
#ax[0].set_xticks(np.arange(-90, 90.1, 30))
#ax[0].set_xticklabels(['90S','60S','30S','EQ','30N','60N','90N'], fontsize=fz)
#ax[0].set_xlim(-90, 90)
#ax[0].set_ylim(30,330)
#ax[0].set_xlabel('Latitude', fontsize=fz)
#ax[0].legend(['Absorbed solar radiation','Outgoing longwave radiation'],
#             edgecolor='white')
#ax[0].set_title('Radiation zonal mean at the TOA in annual mean',
#                fontweight='bold')


#plt.savefig('rad-zonalmean.png')
#plt.show()
