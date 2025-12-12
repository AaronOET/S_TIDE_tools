# Read 2024_1186_東港潮位站_tide.csv
# Extract hourly data (at time :00)
# Organize the data in two columns, where first column is time in YYYY-MM-DD HH:MM format, and tide in unit of meters
# Save the result to TideClean.csv

import pandas as pd

# Read the CSV file
df = pd.read_csv('2016_1486_高雄潮位站_tide.csv', skiprows=20)

# Extract the relevant columns: yyyymmddhh and :00 (hourly data)
tide_data = df[['yyyymmddhh', ':00']].copy()

# Convert yyyymmddhh to datetime format (YYYY-MM-DD HH:MM)


def convert_to_datetime(yyyymmddhh):
    try:
        # Convert to string and ensure it's 10 digits
        date_str = str(int(yyyymmddhh))
        if len(date_str) == 10:
            # Parse YYYYMMDDHH format
            year = date_str[:4]
            month = date_str[4:6]
            day = date_str[6:8]
            hour = date_str[8:10]
            return f"{year}-{month}-{day} {hour}:00"
        else:
            return None
    except Exception:
        return None


# Convert all timestamps, including invalid ones (which will become None)
tide_data['datetime'] = tide_data['yyyymmddhh'].apply(convert_to_datetime)

# Convert tide height from millimeters to meters (this will handle missing/invalid data as NaN)
tide_data['tide_meters'] = pd.to_numeric(
    tide_data[':00'], errors='coerce') / 1000

# Remove rows where datetime conversion failed (only remove truly invalid timestamps)
tide_data = tide_data.dropna(subset=['datetime'])

# Convert datetime column to pandas datetime for proper sorting and resampling
tide_data['datetime'] = pd.to_datetime(tide_data['datetime'])

# Sort by datetime
tide_data = tide_data.sort_values('datetime')

# Create a complete hourly time series starting from Jan-01 of the year to last valid timestamp
first_timestamp = tide_data['datetime'].min()
end_time = tide_data['datetime'].max()
# Set start_time to January 1st 00:00 of the same year as the first timestamp
start_time = pd.Timestamp(year=first_timestamp.year, month=1, day=1, hour=0)
complete_time_series = pd.date_range(start=start_time, end=end_time, freq='h')

# Create a dataframe with the complete time series
complete_df = pd.DataFrame({'datetime': complete_time_series})

# Merge with the original data to fill missing timestamps with NaN
final_data = complete_df.merge(
    tide_data[['datetime', 'tide_meters']], on='datetime', how='left')

# Format datetime back to string format for output
final_data['Time'] = final_data['datetime'].dt.strftime('%Y/%m/%d %H:%M')

# Create the final dataframe with two columns
final_data = final_data[['Time', 'tide_meters']].copy()
final_data.columns = ['Time', 'Tide_m']

# Fill missing values with string "NaN" instead of empty
final_data['Tide_m'] = final_data['Tide_m'].fillna('NaN')

# Save to TideClean.csv
final_data.to_csv('TideClean.csv', index=False, header=False)

# Save to TideClean.txt
final_data.to_csv('TideClean.txt', index=False, sep='\t')


print(
    f"Processing complete. {len(final_data)} hourly tide records saved to TideClean.csv")
print(
    f"Number of valid tide measurements: {(final_data['Tide_m'] != 'NaN').sum()}")
print(
    f"Number of missing timestamps filled with NaN: {(final_data['Tide_m'] == 'NaN').sum()}")
print("\nFirst 10 rows of processed data:")
print(final_data.head(10))
print("\nLast 10 rows of processed data:")
print(final_data.tail(10))
