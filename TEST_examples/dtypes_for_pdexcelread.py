import pandas as pd
import numpy as np

# Column names
columns = [
    'nazva_tmc', 'od_vymiru', 'zal_poch_kilk', 'zal_poch_sum',
    'pryb_kilk', 'pryb_suma', 'vytr_kilk', 'vytr_sum',
    'zal_kilk', 'zal_sum'
]

# Converter function for numeric columns
def convert_numeric(value):
    if value == '' or pd.isna(value):  # Handle empty strings and NaN
        return np.nan
    try:
        return pd.to_numeric(value, errors='coerce')  # Coerce invalid numbers
    except:
        return np.nan

# Apply converters for all numeric columns
converters = {
    'zal_poch_kilk': convert_numeric,
    'zal_poch_sum': convert_numeric,
    'pryb_kilk': convert_numeric,
    'pryb_suma': convert_numeric,
    'vytr_kilk': convert_numeric,
    'vytr_sum': convert_numeric,
    'zal_kilk': convert_numeric,
    'zal_sum': convert_numeric,
    'nazva_tmc': lambda x: x if x != '' else np.nan,  # Handle empty strings in text
    'od_vymiru': lambda x: x if x != '' else np.nan
}

# Read Excel with converters
obs_xlsx_file_path = '/READ_FILES/ZAVDANNIA_TEST/RENKAS_JV/ECOTOXYCOLOGICHYKH/ZVD_2__OBOROTKY/1113.xlsx'

raw_obs_df = pd.read_excel(
    obs_xlsx_file_path,
    converters=converters,
    engine='openpyxl',
    sheet_name=0,
    skiprows=6,
    header=None,
    names=columns
)

# Remove the last row
raw_obs_df = raw_obs_df[:-1]

# Check data types and missing values
print('raw_obs_df.info() -->\n', raw_obs_df.info())
print('Missing values per column:\n', raw_obs_df.isnull().sum())
