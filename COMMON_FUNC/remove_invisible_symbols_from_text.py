import pandas as pd
import regex  # Make sure you installed THIS module, not "regular_regex"


def clean_text_columns(df):
    """ Cleans all text columns in a DataFrame from invisible characters. """

    def clean_text(text):
        if isinstance(text, str):
            return regex.sub(r'[\s\p{C}\u2028\u2029]+', ' ', text).strip()  # Use regex instead of re
        return text

    # Select only text columns (dtype == object)
    text_cols = df.select_dtypes(include=['object']).columns

    # Apply cleaning function to all text columns
    #df[text_cols] = df[text_cols].applymap(clean_text)
    df.loc[:, text_cols] = df.loc[:, text_cols].applymap(clean_text)
    return df

'''
# 🔥 Test DataFrame
df = pd.DataFrame({
    'id': [1, 2, 3],
    'dirty_text': ['Hello\nWorld!', 'Some\ttext with\rweird spaces', 'Clean text'],
    'numeric_col': [100, 200, 300],
    'another_dirty_text': ['Messy \n  text', None, 'Fine\ttoo']
})

print("✅ Before cleaning:\n", df, "\n")

df_clean = clean_text_columns(df)

print("✅ After cleaning:\n", df_clean)'''