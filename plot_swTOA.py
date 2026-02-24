import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import xarray as xr
from pathlib import Path

# Data path
era_path = Path("/home/esp-shared-a/Distribution/Diploma/ESM/data/ESM_2025/ERA5/month")
sw = era_path / 'avg_snswrf_ERA5_1991-2020.nc'

# Open dataset
data = xr.open_dataset(sw)

# Variable (nota: el nombre debe ir como string)
var = data["avg_snswrf"]

# Mean TOA SW radiation
avg_sw = var.mean(dim="valid_time")

# Figure and map projection
fig = plt.figure(figsize=(20, 10))
ax = plt.axes(projection=ccrs.PlateCarree())

# Plot
avg_sw.plot(
    ax=ax,
    x="longitude",
    y="latitude",
    transform=ccrs.PlateCarree(),
    cmap="jet",
    cbar_kwargs={"label": "TOA incoming SW radiation (W/m²)"}
)

# Add coastline and borders
ax.coastlines(resolution="50m", linewidth=1.0)
ax.add_feature(cfeature.BORDERS, linestyle=":", linewidth=0.5)

# Labels and title
ax.set_title("SW radiation (ERA5, 1991–2020)")
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

plt.show()