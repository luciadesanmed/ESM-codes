import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import xarray as xr
from pathlib import Path

# Data path
dat_path = Path("/home/desan/ESM-data/")

#Cases:
#cases = ('pr_annualmean_EC-Earth3.nc', 'pr_annualmean_EC-Earth3-AerChem.nc','pr_annualmean_EC-Earth3-Veg-LR.nc',
#          'pr_annualmean_ERA5.nc', 'tas_annualmean_EC-Earth3.nc', 'tas_annualmean_EC-Earth3-AerChem.nc',
#          'tas_annualmean_EC-Earth3-Veg-LR.nc','tas_annualmean_ERA5.nc', 'rh_annualmean_EC-Earth3.nc',
#          'rh_annualmean_EC-Earth3-AerChem.nc','rh_annualmean_EC-Earth3-Veg-LR.nc', 'rh_annualmean_ERA5.nc')
cases = ('pr_annualmean_EC-Earth3.nc', 'pr_annualmean_EC-Earth3-AerChem.nc','pr_annualmean_EC-Earth3-Veg-LR.nc',
         'tas_annualmean_EC-Earth3.nc', 'tas_annualmean_EC-Earth3-AerChem.nc', 'tas_annualmean_EC-Earth3-Veg-LR.nc',
         'hurs_annualmean_EC-Earth3.nc', 'hurs_annualmean_EC-Earth3-AerChem.nc','hurs_annualmean_EC-Earth3-Veg-LR.nc')

variab = ('pr', 'tas', 'hurs')
cmaps = ('YlGnBu','turbo','YlGnBu') #_r to invert the colormap
nlevels1 = (200, 200, 200) 
vmin1 = (0, -30, 0)
vmax1 = (10.1, 30.1, 100.1)
cticks = (1, 5, 20)
units = ('mm/day', '°C', '%')
cbarext = ('max','both','neither')
exps = ('EC-Earth3 (hist):', 'EC-Earth3-AerChem (hist):', 'EC-Earth3-Veg-LR (hist):')
#exps = ('EC-Earth3 (hist):', 'EC-Earth3-AerChem (hist):', 'EC-Earth3-Veg-LR (hist):', 'ERA5 (1970-2014):')

#Tuple with cases:
texts = ('Precipitation', 'Temperature (surface)', 'Relative humidity (surface)')

nn=0
n1=0 #index for variable - only 3 variables
n2=0 #index for exp - 3 variables

for i in cases:
    # Open dataset
    data = xr.open_dataset(dat_path / i)
    #Variable:
    var = data[variab[n1]]

    if variab[n1]=='pr':
        var=var*86400
    elif variab[n1]=='tas':
        var=var-273.15
        
    # Figure and map projection
    fig = plt.figure(figsize=(20, 10))
    ax = plt.axes(projection=ccrs.Robinson(central_longitude=0))

    #Colormap for segmented colorbar:
    #According to the presentation plots:
    nlevels = nlevels1[n1]
    vmin = vmin1[n1]
    vmax = vmax1[n1]
    levels = np.linspace(vmin, vmax, nlevels + 1)
    cmap = plt.get_cmap(cmaps[n1], nlevels)
    norm = colors.BoundaryNorm(levels, ncolors=cmap.N, clip=False)

    pcm = var.plot(
    ax=ax,
    x="lon",
    y="lat",
    transform=ccrs.PlateCarree(),
    cmap=cmap,
    norm=norm,
    add_colorbar=False)

    cbar = plt.colorbar(
    pcm,
    ax=ax,
    ticks=np.arange(vmin, vmax, cticks[n1]),
    orientation='horizontal',
    pad=0.05,
    fraction=0.05,
    extend=cbarext[n1])

    cbar.set_label(
    texts[n1] + ' ' + units[n1],
    fontsize=16,
    fontweight='bold')

    cbar.ax.tick_params(labelsize=14)

    # Add coastline and borders
    ax.coastlines(resolution="50m", linewidth=1.0)
    ax.add_feature(cfeature.BORDERS, linestyle=":", linewidth=0.5)

    # Gridlines
    gl = ax.gridlines(
    draw_labels=True,
    linewidth=0.5,
    color="black",
    alpha=0.5,
    linestyle="-"
    )
    
    gl.xlabel_style = {'size': 14}
    gl.ylabel_style = {'size': 14}

    # Labels and title
    ax.set_title('Annual mean '+ exps[n2] +' '+ texts[n1], fontsize=20, fontweight='bold')

   # plt.show()
    plt.savefig("annualmean_ECEARTH_"+str(nn)+".png")

    if nn==2 or nn==5:
       n1=n1+1
   
    if n2==2:
       n2=-1

    nn=nn+1
    n2=n2+1

    print(nn)
