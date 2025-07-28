import re

import pandas as pd
from sqlalchemy import create_engine, text
from get_answers_from_input import choose_test_or_real_db
from db_tabs_to_dicts_of_dfs import filter_lst_of_table_names, cre_dict_of_dfs
from join_dicts_of_dfs import l_join_dicts_dfs_by_keys
from re import split
pd.set_option('display.max_rows', None)
engine = choose_test_or_real_db().get('db_engine')
#print(f'{type(engine)} Engine =>',  engine)

# 'inv_src', 'obs_src'

lst_of_obs_src_tabs = filter_lst_of_table_names(engine,'obs_src')
lst_of_inv_src_tabs = filter_lst_of_table_names(engine,'inv_src')
print('lst_of_obs_src_tabs=>', lst_of_obs_src_tabs)
print('lst_of_inv_src_tabs=>', lst_of_inv_src_tabs)

dict_of_obs_tables = cre_dict_of_dfs(engine, lst_of_obs_src_tabs)
dict_of_inv_tables = cre_dict_of_dfs(engine, lst_of_inv_src_tabs)
#print("dict_of_obs_tables =>\n", dict_of_obs_tables)
#print("dict_of_inv_tables =>\n", dict_of_inv_tables)

dict_of_merged_dfs = l_join_dicts_dfs_by_keys(dict_of_obs_tables, dict_of_inv_tables)

'''for k, v in dict_of_merged_dfs.items():
    print('**********')
    print(k,'\n')
    print(v)'''


err_repl_or_app = 'replace'#{‘fail’, ‘replace’, ‘append’}
for table_name, df in dict_of_merged_dfs.items():
    #print(df.head(10))
    df.to_sql(name=table_name, con=engine, index=False,if_exists=err_repl_or_app)



