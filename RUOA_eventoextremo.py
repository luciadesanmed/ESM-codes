import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import matplotlib.dates as mdates

# --- Configuration ---
data_path = Path('/home/desan/RUOA-data') 
file_name = 'RUOA_agsc_2016_03.csv'
fz = 12

# --- 1. Data Loading ---
full_path = data_path / file_name
df = pd.read_csv(full_path, skiprows=6)
df = df.drop(index=0)

# --- 2. Data Preprocessing ---
df['TIMESTAMP'] = pd.to_datetime(df['TIMESTAMP'])
df['Temp_Avg'] = pd.to_numeric(df['Temp_Avg'], errors='coerce')
df['Rain_Tot'] = pd.to_numeric(df['Rain_Tot'], errors='coerce')

# Filter for the 3-day range
start_3d = '2016-03-08 00:00:00'
end_3d = '2016-03-10 23:59:59'
df_3days = df[(df['TIMESTAMP'] >= start_3d) & (df['TIMESTAMP'] <= end_3d)].copy()

# Filter for the specific target day (March 9th)
df_target = df[df['TIMESTAMP'].dt.date == pd.to_datetime('2016-03-09').date()].copy()

# ---------------------------------------------------------
# FIGURE 1: Continuous 3-Day View with Highlight
# ---------------------------------------------------------
fig1, ax1_f1 = plt.subplots(figsize=(14, 6))
ax2_f1 = ax1_f1.twinx()

# Highlight March 9th
ax1_f1.axvspan(pd.Timestamp('2016-03-09 00:00:00'), 
               pd.Timestamp('2016-03-09 23:59:59'), 
               color='yellow', alpha=0.2, label='March 09 (Focus)')

ax1_f1.plot(df_3days['TIMESTAMP'], df_3days['Rain_Tot'], color='blue')
ax2_f1.plot(df_3days['TIMESTAMP'], df_3days['Temp_Avg'], color='y')

ax1_f1.set_title('Overview: March 08 - 10, 2016', fontsize=fz+2, fontweight='bold')
ax1_f1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%b\n%H:%M'))
ax1_f1.set_ylabel('Precipitation (mm/hour)', color='blue', fontweight='bold')
ax2_f1.set_ylabel('Temperature (°C)', color='red', fontweight='bold')
ax1_f1.grid(True, linestyle='--', alpha=0.3)

# Legend for Fig 1
h1, l1 = ax1_f1.get_legend_handles_labels()
h2, l2 = ax2_f1.get_legend_handles_labels()
ax1_f1.legend(h1+h2, l1+l2, loc='upper left')

# ---------------------------------------------------------
# FIGURE 2: Detailed Target Day (March 9th)
# ---------------------------------------------------------
fig2, ax1_f2 = plt.subplots()
ax2_f2 = ax1_f2.twinx()

# Plot single day data
mth = np.arange(1, 24.1, 1) #24 hours

ax1_f2.plot(mth, df_target['Rain_Tot'], 
            color='blue', markersize=4)
ax2_f2.plot(mth, df_target['Temp_Avg'], 
            color='y', markersize=4)

ax1_f2.set_title('RUOA station: 9 march 2016', fontsize=fz+2, fontweight='bold')
#ax1_f2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax1_f2.set_xlabel('Hour', fontweight='bold')
ax1_f2.set_ylabel('Precipitation (mm/hour)', color='blue', fontweight='bold')
ax2_f2.set_ylabel('Temperature (°C)', color='y', fontweight='bold')
ax2_f2.tick_params(axis='y', labelcolor='y',color='y')
ax1_f2.tick_params(axis='y', labelcolor='b',color='b')
ax1_f2.set_xticks(np.arange(1, 25, 1)) # Labels for every single hour

#ax1_f2.grid(True, linestyle=':', alpha=0.6)

# Legend for Fig 2
h3, l3 = ax1_f2.get_legend_handles_labels()
h4, l4 = ax2_f2.get_legend_handles_labels()
ax1_f2.legend(h3+h4, l3+l4, loc='upper right')

plt.tight_layout()
plt.savefig('ruoa_extreme.png')
