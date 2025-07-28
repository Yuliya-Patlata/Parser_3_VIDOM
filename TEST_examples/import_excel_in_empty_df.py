import pandas as pd
import numpy as np
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
# Define column names and their data types
dtype_mapping = {
    'nazva_tmc': 'object',
    'od_vymiru': 'object',
    'zal_poch_kilk': 'float32',
    'zal_poch_sum': 'float32',
    'pryb_kilk': 'float32',
    'pryb_suma': 'float32',
    'vytr_kilk': 'float32',
    'vytr_sum': 'float32',
    'zal_kilk': 'float32',
    'zal_sum': 'float32'
}

# Step 1: Create an empty DataFrame with specified dtypes
clean_df = pd.DataFrame({col: pd.Series(dtype=dtype) for col, dtype in dtype_mapping.items()})

# Step 2: Read raw data from Excel (without dtype enforcement)
obs_xlsx_file_path = '/READ_FILES/ZAVDANNIA_TEST/RENKAS_JV/ECOTOXYCOLOGICHYKH/ZVD_2__OBOROTKY/1113.xlsx'

raw_data = pd.read_excel(
    obs_xlsx_file_path,
    engine='openpyxl',
    sheet_name=0,
    skiprows=6,
    header=None,
    names=list(dtype_mapping.keys())
)

# Step 3: Fill the clean DataFrame with converted data
for col in clean_df.columns:
    if clean_df[col].dtype == 'float32':
        # Convert to numeric, handle errors, and ensure float32
        clean_df[col] = pd.to_numeric(raw_data[col], errors='coerce').astype('float32')
    else:
        # For object columns, handle empty strings
        clean_df[col] = raw_data[col].apply(lambda x: x if pd.notna(x) else np.nan)

# Step 4: Remove the last row if needed
clean_df = clean_df[:-1]

# Step 5: Display info
print('clean_df.info() -->\n', clean_df.info())
print('Missing values per column:\n', clean_df.isnull().sum())
print('clean_df=>', clean_df)

