import pandas as pd
import matplotlib.pyplot as plt
import os
import glob

# Configuration
directory_path = '/home/desan/RUOA-data'
years = range(2015, 2026)
months = ['07', '12']
cols_of_interest = ['Temp_Avg', 'Rain_Tot']

def process_ruoa_data():
    all_data = []
    file_pattern = os.path.join(directory_path, "RUOA_agsc_*.csv")
    files = glob.glob(file_pattern)
    
    for file_path in files:
        filename = os.path.basename(file_path)
        parts = filename.replace('.csv', '').split('_')
        if len(parts) < 4: continue
        
        year_str, month_str = parts[2], parts[3]
        if not (year_str.isdigit() and int(year_str) in years and month_str in months):
            continue
            
        if os.stat(file_path).st_size == 0:
            continue
            
        try:
            # Metadata skip: header row 6, units row 7
            df = pd.read_csv(file_path, skiprows=6)
            if df.empty: continue
            df = df.drop(index=0) # Drop units row
            
            df['TIMESTAMP'] = pd.to_datetime(df['TIMESTAMP'])
            
            # Get Hour (0-23)
            df['Hour'] = df['TIMESTAMP'].dt.hour
            
            # Shift 0 to 24 so the day ends at 24
            df['Hour'] = df['Hour'].replace(0, 24)
            
            df['Month'] = df['TIMESTAMP'].dt.month
            
            for col in cols_of_interest:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            all_data.append(df[['Month', 'Hour', 'Temp_Avg', 'Rain_Tot']])
        except Exception as e:
            print(f"Error processing {filename}: {e}")

    if not all_data: return None

    # Concatenate and calculate hourly averages
    full_df = pd.concat(all_data, ignore_index=True)
    
    # Group and sort by hour (1, 2, ..., 23, 24)
    hourly_means = full_df.groupby(['Month', 'Hour'])[['Temp_Avg', 'Rain_Tot']].mean().reset_index()
    hourly_means = hourly_means.sort_values(['Month', 'Hour'])
    
    return hourly_means

def plot_data(hourly_means):
    if hourly_means is None: return

    fig, ax1 = plt.subplots(figsize=(12, 8))
    ax2 = ax1.twinx() # Right axis for Temperature
    
    month_names = {7: 'July', 12: 'December'}
    styles = {
            7: {'temp': '-', 'rain': '-'},
        12: {'temp': '--', 'rain': '--'}
    }
    
    for month in [7, 12]:
        m_data = hourly_means[hourly_means['Month'] == month]
        if m_data.empty: continue
        
        # Scaling Precipitation by 24 (hourly value scaled to daily rate)
        rain_scaled = m_data['Rain_Tot'] * 24
        
        # Left Axis: Precipitation (Scaled)
        ax1.plot(m_data['Hour'], rain_scaled, 
                 linestyle=styles[month]['rain'], color='tab:blue', linewidth=1.5,
                label=f"Rain {month_names[month]} (Scaled $\\times$ 24)")
        
        # Right Axis: Temperature
        ax2.plot(m_data['Hour'], m_data['Temp_Avg'], 
                linestyle=styles[month]['temp'], color='y', linewidth=2,
                label=f"Mean Temp {month_names[month]}")

    ax1.set_xlabel('Hour of Day (1-24)', fontsize=12)
    ax1.set_ylabel('Precipitation (mm/day)', color='tab:blue', fontsize=12)
    ax2.set_ylabel(r'Temperature ($^{\circ}$C)', color='y', fontsize=12)
    
    plt.title('Hourly Mean RUOA station (2015-2025)', fontsize=14)
    
    # Combined legend
    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1 + h2, l1 + l2, loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=2)
    
    # Set x-ticks from 1 to 24 and set x-limits
    ax1.set_xticks(range(1, 25))
    ax1.set_xlim(0.5, 24.5)
    ax1.grid(True, linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    #plt.savefig('precipitation_shifted_plot.png')
    plt.show()

# Execute analysis
results = process_ruoa_data()
if results is not None:
    plot_data(results)
