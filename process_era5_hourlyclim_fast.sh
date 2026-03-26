#!/bin/bash

# --- Configuration ---
INPUT_DIR="/afs/ictp.it/home/a/ade_sant/ERA5"
OUTPUT_FILE="sshf_ags_jul_hourlyclim.nc"
BOX="257.052264,258.204600,21.5139417,22.4147556"

echo "Processing all years in a single high-speed stream..."

# 1. Chain all operations: 
# Select Area -> Shift Time -> Field Mean -> Merge All Decembers -> Final Hourly Mean
cdo -fldmean -shifttime,-6hour -sellonlatbox,$BOX \
    -mergetime $INPUT_DIR/sshf_ERA5_*_07.nc \
    all_decembers_combined.nc

echo "Splitting and averaging (Fail-safe logic)..."

# 2. Use a temporary directory for the split (very fast on small files)
mkdir -p tmp_split && cd tmp_split
cdo splithour ../all_decembers_combined.nc hour_

for f in hour_??.nc; do 
    cdo timmean $f m_$f
done

cdo -O mergetime m_hour_??.nc "../$OUTPUT_FILE"

# 3. Cleanup
cd ..
rm -rf tmp_split all_decembers_combined.nc

echo "Done! Processed into 24 steps: $OUTPUT_FILE"
