import pandas as pd
import numpy as np
from sqlalchemy import text, engine
from get_answers_from_input import *

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
#pd.set_option('display.max_rows', None)
dict_of_input_params = choose_test_or_real_db()
engine = dict_of_input_params.get('db_engine')
tablename = 'public.inv_src_10__01_02_25'
query = text(f'SELECT * FROM {tablename};')

with engine.connect() as con:
    result = con.execute(query)
    # rows = result.fetchall()
    # print('type(rows)=>', type(rows))
    lst_rows_of_dicts = [dict(row) for row in result.mappings().fetchall()]
    df_10_inv = pd.DataFrame(lst_rows_of_dicts)
    years = ['2002','2003','2004', '2005', '2006', '2007','2008', '2009']
    filtered_df = df_10_inv[(df_10_inv['inv_no_range'].apply(lambda x: len(x) > 9)) & (df_10_inv['inv_no_range'].str[0:4] =='1016') & (df_10_inv['rik'].isin(years)) ]

print('df_10_inv=>\n', df_10_inv)
print('filtered_df=>\n', filtered_df)