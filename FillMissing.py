import pandas as pd
import numpy as np

def fill_missing_data():
    """
    Fill missing data in TideClean.csv using Hindcast values from 'Observation and Hindcast.txt'
    and output to TideResult.csv with original data and an extra column
    """
    
    # Read TideClean.csv
    print("Reading TideClean.txt...")
    tide_df = pd.read_csv('TideClean.txt', sep='\t')
    tide_df['Time'] = pd.to_datetime(tide_df['Time'])
    print(f"TideClean.txt loaded: {len(tide_df)} records")
    print(f"Missing values in Tide_m: {tide_df['Tide_m'].isna().sum()}")
    
    # Read Observation and Hindcast.txt
    print("\nReading Observation and Hindcast.txt...")
    hindcast_df = pd.read_csv('Observation and Hindcast.txt', sep=r'\s+')
    print(f"Hindcast data loaded: {len(hindcast_df)} records")
    
    # Create a copy of the original data for the result
    result_df = tide_df.copy()
    
    # Add the Hindcast column to match the observations
    # Assuming the data is in chronological order and corresponds 1:1
    if len(hindcast_df) >= len(tide_df):
        result_df['Hindcast'] = hindcast_df['Hindcast'].iloc[:len(tide_df)].values
    else:
        # If hindcast data is shorter, pad with NaN
        hindcast_values = list(hindcast_df['Hindcast'].values) + [np.nan] * (len(tide_df) - len(hindcast_df))
        result_df['Hindcast'] = hindcast_values
    
    # Create a filled version of Tide_m using Hindcast for missing values
    result_df['Tide_m_filled'] = result_df['Tide_m'].fillna(result_df['Hindcast'])
    
    # Show statistics
    original_missing = tide_df['Tide_m'].isna().sum()
    filled_missing = result_df['Tide_m_filled'].isna().sum()
    filled_count = original_missing - filled_missing
    
    print("\nData filling summary:")
    print(f"Original missing values: {original_missing}")
    print(f"Values filled with Hindcast: {filled_count}")
    print(f"Remaining missing values: {filled_missing}")
    
    # Reorder columns for better readability
    result_df = result_df[['Time', 'Tide_m', 'Hindcast', 'Tide_m_filled']]
    
    # Save to TideResult.csv
    result_df.to_csv('TideResult.csv', index=False)
    print(f"\nResults saved to TideResult.csv with {len(result_df)} records")
    
    # Display some examples of filled data
    filled_examples = result_df[tide_df['Tide_m'].isna()].head(10)
    if not filled_examples.empty:
        print("\nFirst 10 examples of filled missing values:")
        print(filled_examples[['Time', 'Tide_m', 'Hindcast', 'Tide_m_filled']])
    
    return result_df

def analyze_results():
    """
    Analyze the results and show some statistics
    """
    try:
        result_df = pd.read_csv('TideResult.csv')
        result_df['Time'] = pd.to_datetime(result_df['Time'])
        
        print("\nTideResult.csv Analysis:")
        print("=" * 50)
        print(f"Total records: {len(result_df)}")
        print(f"Date range: {result_df['Time'].min()} to {result_df['Time'].max()}")
        print("\nColumn statistics:")
        print(result_df[['Tide_m', 'Hindcast', 'Tide_m_filled']].describe())
        
        print("\nMissing values by column:")
        print(f"Tide_m: {result_df['Tide_m'].isna().sum()}")
        print(f"Hindcast: {result_df['Hindcast'].isna().sum()}")
        print(f"Tide_m_filled: {result_df['Tide_m_filled'].isna().sum()}")
        
    except FileNotFoundError:
        print("TideResult.csv not found. Please run fill_missing_data() first.")

if __name__ == "__main__":
    # Execute the filling process
    result_data = fill_missing_data()
    
    # Analyze the results
    analyze_results()