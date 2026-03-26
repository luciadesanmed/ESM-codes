#!/bin/bash
#pev december hourly climatology:
cdo -fldmean -dhourmean -shifttime,-6hours -selmonth,12 -mergetime era5_pev_*.nc pev_ags_dec_hourlyclim.nc

#pev july hourly climatology:
cdo -fldmean -dhourmean -shifttime,-6hours -selmonth,7 -mergetime era5_pev_*.nc pev_ags_jul_hourlyclim.nc

#sshf dec hourly climatology, doing change for w/m2:
cdo -divc,3600 -fldmean -dhourmean -shifttime,-6hours -selmonth,12 -mergetime era5_sshf_*.nc sshf_ags_dec_hourlyclim.nc

#sshf jul hourly climatology, change for w/m2:
cdo -divc,3600 -fldmean -dhourmean -shifttime,-6hours -selmonth,7 -mergetime era5_sshf_*.nc sshf_ags_jul_hourlyclim.nc

#slhf dec hourly climatology, doing change for w/m2:
cdo -divc,3600 -fldmean -dhourmean -shifttime,-6hours -selmonth,12 -mergetime era5_slhf_*.nc slhf_ags_dec_hourlyclim.nc

#slhf jul hourly climatology, change for w/m2:
cdo -divc,3600 -fldmean -dhourmean -shifttime,-6hours -selmonth,7 -mergetime era5_slhf_*.nc slhf_ags_jul_hourlyclim.nc

#heat storage, dec:
cdo enssum sshf_ags_dec_hourlyclim.nc slhf_ags_dec_hourlyclim.nc ags-sum-sens-lat-heat-dec.nc

cdo enssum ssr_ags_dec_hourlyclim.nc ags-sum-sens-lat-heat-dec.nc heatstor_ags_dec.nc

#heat storage, july:
cdo enssum sshf_ags_jul_hourlyclim.nc slhf_ags_jul_hourlyclim.nc ags-sum-sens-lat-heat-jul.nc

cdo enssum ssr_ags_jul_hourlyclim.nc ags-sum-sens-lat-heat-jul.nc heatstor_ags_jul.nc
