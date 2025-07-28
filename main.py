import pandas as pd
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
#pd.set_option('display.max_rows', None)
# нижче імпортуємо наші модулі рекурсивного пробігу по папках з файлами
from folder_recursive_files_list import *
from path_handler_to_file_attrs_dict import *
from cre_dicts import *

from get_answers_from_input import choose_test_or_real_db
# нижче імпортуємо наші модулі для обробки інвентарних  описів
from universal_col_df_10_11_15_18 import *
from writers_to_sep_10_11_15_18_XX import *
from dfs_concat_by_condition import *
# нижче імпортуємо наші модулі для обробки обороток
from raw_obs_xlsx_reader import *
from univ_obs_column_prep import *
from obs_df_concat_by_XX_rahunku import *

from obs_range_splitter_10_11 import *
from obs_writers_to_sep_10_11_15_18_XX import *
from inv_10_src_db_tab_rename_split import *
#functions for getting db tables and left merging dicts of obs and inv dfs
from db_tabs_to_dicts_of_dfs import filter_lst_of_table_names, cre_dict_of_dfs
from join_dicts_of_dfs import l_join_dicts_dfs_by_keys


if __name__ == '__main__':
    dict_of_input_params = choose_test_or_real_db()
    engine = dict_of_input_params.get('db_engine')
    READ_START_of_nested_dirs = dict_of_input_params.get('read_start_path')
    WRITE_START_of_nested_dirs = dict_of_input_params['write_start_path']

    file_description_lst_of_dicts = folder_recursive_path_parts_dict_maker(READ_START_of_nested_dirs)
    #print('file_description_lst_of_dicts=>\n', file_description_lst_of_dicts)

    files_attrs_lst = folder_recursive_path_parts_list_maker(READ_START_of_nested_dirs)
    #pprint.pp(result_lst)
    #dd_mm_yy = input(f'Введіть дату формування інвентарних відомостей dd_mm_yy =>')
    dd_mm_yy = '01_02_25'

    dict_of_total_inv_dfs = cre_dict_of_total_inv_dfs()
    dict_of_total_obs_dfs = cre_dict_of_total_obs_dfs()

    #print('*****\n', 'dict_of_total_inv_dfs =>', dict_of_total_inv_dfs)
    for i in range(0,len(files_attrs_lst)):
        #print(f'files_attrs_lst[{i}]=>',files_attrs_lst[i][0],'\t', files_attrs_lst[i][1],'\t', files_attrs_lst[i][2])
        zvd_no_nazva = files_attrs_lst[i][0]
        #print('zvd_no_nazva =>', zvd_no_nazva )
        if zvd_no_nazva =='ZVD_1__INV_OPYSY':
            #pass

            raw_inv_df = skip_rows_file_name_parser(files_attrs_lst[i])
            #print(files_attrs_lst[i][2])

            trimmed_df = end_trimmer(raw_inv_df)
            #print('trimmed_df.columns =>', trimmed_df.columns)
            #print()
            #print('trimmed_df["012"]=>\n', trimmed_df.head(10))
            univ_inv_df = convert_to_universal_df( dd_mm_yy, trimmed_df, files_attrs_lst[i])
            #print(f'i={i} \t univ_df ')
            #pprint.pp(univ_inv_df)
            writers_to_separate_files(univ_inv_df, files_attrs_lst[i] )

            dict_of_total_inv_dfs = univ_inv_dfs_concat_by_condition(dict_of_total_inv_dfs, univ_inv_df,files_attrs_lst[i] )

            #for key, value in dict_of_total_inv_dfs.items():
            #    print(f'{i}=', key, '\ndf value=>\n', value)

            writer_of_dict_of_total_inv_dfs(dict_of_total_inv_dfs, WRITE_START_of_nested_dirs)
            #print()
            #print('dict_of_total_inv_dfs=>\n', dict_of_total_inv_dfs)

        elif zvd_no_nazva == 'ZVD_2__OBOROTKY':

            #print('ZVD_2__OBOROTKY')
            #print(zvd_no_nazva)
            print(f'files_attrs_lst[{i}]=>', files_attrs_lst[i][0], '\t', files_attrs_lst[i][1], '\t', files_attrs_lst[i][2], '\t', files_attrs_lst[i][3])
            raw_obs_df = raw_obs_xlsx_reader(files_attrs_lst[i])
            additional_col_val_dict = columns_to_add(files_attrs_lst[i])
            #print('additional_col_val_dict=>', additional_col_val_dict)
            univ_obs_df= cre_univ_obs_df(raw_obs_df, files_attrs_lst[i][-1], additional_col_val_dict )
            #print('univ_obs_df=>\n', univ_obs_df)
            obs_writers_to_separate_files(univ_obs_df, files_attrs_lst[i])
            dict_of_obs_dfs_conc_by_xx = univ_obs_df_concat_by_xx_rahunku(dict_of_total_obs_dfs, univ_obs_df, files_attrs_lst[i])
            xlsx_writer_of_dict_conc_obs_univ_dfs(dict_of_obs_dfs_conc_by_xx, WRITE_START_of_nested_dirs )


        elif zvd_no_nazva == 'ZVD_3__OBOROTKY_BY_TOPICS':
            pass
        else: print('Unknown zvd_no_nazva')

    # PostgreSQL connection string
    inv_table_name_suffix = dd_mm_yy
    err_repl_or_app = 'replace'#{‘fail’, ‘replace’, ‘append’}

    for table_name, df in dict_of_total_inv_dfs.items():
        tab_name = 'inv_src_' + table_name +'__' + inv_table_name_suffix
        #print('tab_name=>', tab_name)
        #print(df.head(10))
        df.to_sql(name=tab_name, con=engine, index=False,if_exists=err_repl_or_app)

    inv_10_range_spliter(engine, 'inv_src_10__01_02_25')

    obs_table_name_suffix = '__10_02_25'
    err_repl_or_app = 'replace'#{‘fail’, ‘replace’, ‘append’}

    for table_name, df in dict_of_obs_dfs_conc_by_xx.items():
        tab_name = 'obs_src_' + table_name + obs_table_name_suffix
        #print('tab_name=>', tab_name)
        #print(df.head(10))
        df.to_sql(name=tab_name, con=engine, index=False,if_exists=err_repl_or_app)
