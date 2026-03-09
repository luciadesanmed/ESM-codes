import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import matplotlib.colors as mcolors
from pathlib import Path

# Data path
era_path = Path("/home/desan/ESM-data/")
pet = era_path / 'ags-avg-pot-evap.nc'
p = era_path / 'ags-avg-prec.nc'
e = era_path / 'ags-avg-evap.nc'

cases = (pet, p, e)
varc = ('pev', 'tp','e')

#latmin =  21.5139417 #21°30'50.19"N
#latmax =  22.4147556 #22°24'53.12"N
#lonmin = 257.052264 #102°56'51.85"O -102.947736
#lonmax = 258.204600 #101°47'43.44"O -101.7953997

n=0
var = [  ]
for i in cases:
    data = xr.open_dataset(i)
    dat = data[varc[n]].squeeze()
    var.append(dat)
    n = n+1

mth = np.arange(1, 12.1, 1) #12 months

fz = 12

plt.plot(mth, -1000*var[0],
          color='k',
           linestyle='-')
plt.plot(mth, 1000*var[1],
           color='b',
           linestyle='--')
plt.plot(mth, -1000*var[2],
         color='r',
         linestyle='--')
plt.xlabel("Month", fontsize=fz, fontweight='bold')
plt.ylabel(r" mm day$^{-1}$", fontsize=fz, fontweight='bold')
#plt.yticks(np.arange(-50,300.1,50))
plt.xticks(np.arange(1, 12.1, 1), labels=['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'], fontsize=fz)
#plt.ylim(-49, 300)
plt.legend(['PET','P','E'],
             edgecolor='white')
plt.title('Terrestrial water balance (ERA5 1991-2020) \nAguascalientes, Mexico',
                fontweight='bold')


plt.savefig('ags-hydro.png')
#plt.show()
