import cdsapi

client = cdsapi.Client()
dataset = "reanalysis-era5-single-levels"

# Define the range of years
years = [str(year) for year in range(2011, 2021)]

for year in years:
    print(f"Starting download for year: {year}")
    
    # Updated filename to reflect the specific variable
    target_file = f"era5_pev_{year}.nc"
    
    request = {
        "product_type": ["reanalysis"],
        "variable": ["potential_evaporation"], # Changed from mean flux
        "year": [year],
        "month": ["07", '12'],
        "day": [f"{d:02d}" for d in range(1, 32)],
        "time": [f"{h:02d}:00" for h in range(24)],
        "data_format": "netcdf",
        "download_format": "unarchived",
        "area": [22.4147556, 257.052264, 21.5139417, 258.2046]
    }

    try:
        client.retrieve(dataset, request).download(target_file)
        print(f"Finished: {target_file}")
    except Exception as e:
        print(f"Error downloading {year}: {e}")

print("All downloads complete.")
