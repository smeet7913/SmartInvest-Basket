import pandas as pd
import numpy as np

# Load the original CSV file
file_path = 'company.csv'  # Replace with your original file path
df = pd.read_csv(file_path)

# Define the theme to filter
selected_theme = "Midcap"  # Change this to the theme you want to filter

# Filter only stocks that match the selected theme
filtered_df = df[df['Theme'].str.strip().str.lower() == selected_theme.lower()].copy()

# Replace placeholders with NaN in the copied DataFrame
filtered_df.replace(['n/a', 'Data not found', '-', ''], np.nan, inplace=True)

# Remove commas from all string/object columns
filtered_df = filtered_df.apply(lambda x: x.str.replace(',', '', regex=True) if x.dtype == 'object' else x)

# Remove % from all string/object columns
filtered_df = filtered_df.apply(lambda x: x.str.replace('%', '', regex=True) if x.dtype == 'object' else x)

# Columns to exclude from conversion
exclude_columns = ['Stock Symbol', 'Theme']  # 'Expert Recommendation' removed as per your decision

# Convert all other columns to float and round to 2 decimal places
for column in filtered_df.columns:
    if column not in exclude_columns:
        filtered_df[column] = pd.to_numeric(filtered_df[column], errors='coerce').round(2)

# Save the cleaned and filtered data to a new CSV file
filtered_file_path = 'Midcap.csv'
filtered_df.to_csv(filtered_file_path, index=False)

print(f"Filtered and cleaned data for theme '{selected_theme}' has been saved to '{filtered_file_path}'")
print(filtered_df.dtypes)
