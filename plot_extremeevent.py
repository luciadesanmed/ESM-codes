import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import matplotlib.colors as mcolors
from pathlib import Path

# Data path
era_path = Path("/home/desan/ESM-data/")
pet = era_path / 'ags-avg-pot-evap-9mar2016.nc'
p = era_path / 'ags-avg-prec-9mar2016.nc'
e = era_path / 'ags-avg-evap-9mar2016.nc'
temp = era_path / 'ags-avg-temp-9mar2016.nc'

cases = (pet, p, e, temp)
varc = ('pev', 'tp','e', 't2m')

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

mth = np.arange(1, 24.1, 1) #24 hours

fz = 12
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()

ax1.plot(mth, -1000*var[0],
          color='k',
           linestyle='-')
ax1.plot(mth, 1000*var[1],
           color='b',
           linestyle='--')
ax1.plot(mth, -1000*var[2],
         color='r',
         linestyle='--')
ax1.set_xlabel("Hour", fontsize=fz, fontweight='bold')
ax1.set_ylabel(r" mm/hour", fontsize=fz, fontweight='bold')
#plt.yticks(np.arange(-50,300.1,50))
ax1.set_xticks(np.arange(1, 24.1, 1))
#plt.ylim(-49, 300)
ax2.plot(mth, var[3]-273.15,
         color='y',
         linestyle='--')
ax1.legend(['PET','P','E'],
             edgecolor='white')
ax2.set_ylabel('Temperature (°C)', fontsize=fz, fontweight='bold', color='y')
ax2.tick_params(axis='y', labelcolor='y')
#ax1.legend('T', edgecolor='white')
plt.title('Terrestrial water balance (ERA5: 9 march 2016) \nAguascalientes, Mexico',
                fontweight='bold')


plt.savefig('prec_extremeevent.png')
#plt.show()
