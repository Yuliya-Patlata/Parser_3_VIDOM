import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
#import inv_range_splitter_10
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


db_con_str ='postgresql+psycopg2://lucid:1@localhost:5432/ula_test'

obs_query=text("SELECT * FROM obs_src_11__10_02_25;")

table_name = 'l1'+'_'+'inv_src_10__01_02_25'
err_repl_or_app = 'replace'#{‘fail’, ‘replace’, ‘append’}
engine = create_engine('postgresql+psycopg2://lucid:1@localhost:5432/ula_test')
inv_df_spl.to_sql(name=table_name, con=engine, index=False, if_exists=err_repl_or_app)


obs_df = pd.read_sql_query(
    sql= obs_query,
    con=db_con_str
)

def obs_psc_inv_no_spliter_1016_11xx_1812(obs_df_11_1812):
    df = obs_df
    print(df.info())
    df.loc[:, 'inv_no'] = df.inv_no_range
    #Отримуємо список словників кожного рядка  датафрейму
    lst_dict_4_splitting = df.to_dict('records')
    splitted_lst_of_dicts = []
    for row in lst_dict_4_splitting:
        group_inv_no = row.get('inv_no')[0:10]
        if row.get('zal_kilk') > 0 :
            iter_depth = int(row.get('zal_kilk'))
            for i in range(0, iter_depth):
                new_row = row.copy()
                new_row['psc_inv_no'] = f'{group_inv_no}_{i + 1}_of_{iter_depth}'
                splitted_lst_of_dicts.append(new_row)

        else:
            continue # потім додамо цей рядок без змін

    spl_df = pd.DataFrame(splitted_lst_of_dicts)

    return spl_df

obs_spl_res = obs_psc_inv_no_spliter_11_18(obs_df)
print('obs_spl_res=>', obs_spl_res )

table_name = 'l2'+'_'+'obs_src_11__10_02_25'
err_repl_or_app = 'replace'#{‘fail’, ‘replace’, ‘append’}
engine = create_engine('postgresql+psycopg2://lucid:1@localhost:5432/ula_test')
obs_spl_res.to_sql(name=table_name, con=engine, index=False, if_exists=err_repl_or_app)
#obs_df_spl = inv_range_splitter_11(db_con_str, obs_query)

