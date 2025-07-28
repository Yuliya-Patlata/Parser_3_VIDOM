import pandas as pd
from pandas import isnull


#dict_of_merged_dfs = l_join_dicts_dfs_by_keys(dict_of_obs_tables, dict_of_inv_tables)
def key_extractor(tablename_key):
    pure_key= tablename_key.split('__')[0][-2:]
    return pure_key

def l_join_dicts_dfs_by_keys(left_dict, right_dict):
    lj_dict_of_dfs ={}
    pure_r_keys = map(key_extractor, right_dict.keys())
    for l_key in left_dict.keys():
        if key_extractor(l_key) in pure_r_keys:
            #print(f'{l_key }')
            for r_key in right_dict.keys():
                if key_extractor(l_key) == key_extractor(r_key):
                    print(f'{l_key} --> {r_key}')
                    l_df = left_dict.get(l_key)
                    r_df = right_dict.get(r_key)
                    if l_df.empty or r_df.empty or l_df.shape[1]==0 or r_df.shape[1]==0:
                        print(f"Skipping merge for {l_key} --> {r_key} because one of the DataFrames is empty.")
                        continue
                    else:
                        l_df = l_df.add_prefix('o_')
                        r_df = r_df.add_prefix('i_')
                        lj_tablename = 'l1_obs_lj_inv_' + key_extractor(l_key)

                        lj_df = pd.merge(left = l_df, right = r_df,
                                         left_on='o_inv_no',
                                         right_on='i_inv_no',
                                         how='left')
                        lj_df.loc[:,'o_psc_inv_no'] = lj_df[['o_inv_no','o_zal_kilk']].apply( lambda row: f"{row['o_inv_no']}_spysano" if pd.isnull(row['o_zal_kilk']) else f"{row['o_inv_no']}_all_of_{int(row['o_zal_kilk'])}",axis=1)
                        print(f'{lj_tablename} =>\n', lj_df)
                        lj_dict_of_dfs.__setitem__(lj_tablename, lj_df)
                        #lj_dict_of_dfs[lj_tablename] = lj_df
    return lj_dict_of_dfs








