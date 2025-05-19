import pandas as pd
import numpy as np

def process_mansfield_data(input_file, output_file, avg_output_file):
    # Read the raw data, setting index_col=0 to use the winter season as index
    df = pd.read_csv(input_file, index_col=0)
    
    # Melt the dataframe to convert from wide to long format
    df = df.reset_index()  # This creates a column with the winter seasons
    # The column is already named 'year' in the CSV
    df = pd.melt(df, id_vars=['year'], var_name='day_of_winter', value_name='depth_inches')
    
    # Rename year to winter for consistency
    df = df.rename(columns={'year': 'winter'})
    
    # Convert day_of_winter from M/D format to day number
    df['day_of_winter'] = pd.to_datetime('2024-' + df['day_of_winter'], format='%Y-%m/%d').dt.dayofyear
    df.loc[df['day_of_winter'] < 244, 'day_of_winter'] += 365  # Adjust days before September 1 (day 244)
    df['day_of_winter'] = df['day_of_winter'] - 244 + 1  # Make September 1 day 1
    
    # Handle empty strings and convert to float
    df['depth_inches'] = df['depth_inches'].replace('', np.nan).astype(float)
    
    # Convert inches to centimeters
    df['depth_cm'] = df['depth_inches'] * 2.54
    
    # Calculate the date for each measurement
    def get_date(row):
        winter_start_year = int(row['winter'].split('-')[0])
        if row['day_of_winter'] <= 153:  # Approximately November 1 to March 31
            return pd.Timestamp(year=winter_start_year, month=11, day=1) + pd.Timedelta(days=row['day_of_winter'] - 1)
        else:  # April 1 to October 31
            return pd.Timestamp(year=winter_start_year + 1, month=4, day=1) + pd.Timedelta(days=row['day_of_winter'] - 153 - 1)
    
    df['date'] = df.apply(get_date, axis=1)
    
    # Extract date components
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['month_day'] = df['date'].dt.strftime('%m-%d')
    
    # Save processed data
    df.to_csv(output_file, index=False)
    
    # Calculate historical averages (excluding NaN values)
    avg_by_day = df.groupby('day_of_winter')['depth_cm'].mean().reset_index()
    avg_by_day.to_csv(avg_output_file, index=False)

if __name__ == "__main__":
    input_file = "../public/MansfieldDepth.csv"
    output_file = "../public/cleaned_mansfield_snowdepth.csv"
    avg_output_file = "../public/mansfield_historical_averages.csv"
    
    process_mansfield_data(input_file, output_file, avg_output_file) 