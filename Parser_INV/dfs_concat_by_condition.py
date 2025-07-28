from shutil import posix
import pandas as pd
import pathlib
import posixpath
from pathlib import Path
import os
import pprint
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

def univ_inv_dfs_concat_by_condition(dict_of_total_inv_dfs,univ_df, file_attribs_lst ):
    dict_of_total_inv_dfs = dict_of_total_inv_dfs
    univ_df = univ_df
    file_attrs_lst = file_attribs_lst
    #print('file_attrs_lst=>', file_attrs_lst)
    filename_without_ext = file_attrs_lst[-2]

    if filename_without_ext[0:2] in ['10','11','18', '15']:
        key = filename_without_ext[0:2]
        '''
        df = dict_of_total_inv_dfs.get(key)
        print('df =>', df)
        print('type(df)=>', type(df))
        '''
        dict_of_total_inv_dfs[key] = pd.concat([dict_of_total_inv_dfs[key], univ_df], ignore_index=True, axis=0 )
    else:
        key='xx'
        dict_of_total_inv_dfs[key] = pd.concat([dict_of_total_inv_dfs[key], univ_df], ignore_index=True, axis=0)

    #print('dict_of_total_inv_dfs=>\n', dict_of_total_inv_dfs)

    return dict_of_total_inv_dfs


def writer_of_dict_of_total_inv_dfs(dict_of_total_inv_dfs, WRITE_START_of_nested_dirs):
    dict_of_total_inv_dfs = dict_of_total_inv_dfs
    write_path_str = WRITE_START_of_nested_dirs
    #directory = posixpath.dirname(write_path_str)
    p = pathlib.PurePath(write_path_str)
    list_of_parts = list(p.parts)

    first_part_of_path_to_write = list_of_parts
    #print('first_part_of_path =>', first_part_of_path_to_write )

    middle_part_of_path_to_write_xlsx = ['INV_OPYSY', 'CONCAT_BY_2DIGITS', 'XLSX']
    middle_part_of_path_to_write_odf = ['INV_OPYSY', 'CONCAT_BY_2DIGITS', 'ODF']
    middle_part_of_path_to_write_pkl = ['INV_OPYSY', 'CONCAT_BY_2DIGITS', 'PKL']

    dir_path_to_write_xlsx = first_part_of_path_to_write + middle_part_of_path_to_write_xlsx
    dir_path_to_write_odf = first_part_of_path_to_write + middle_part_of_path_to_write_odf
    dir_path_to_write_pkl = first_part_of_path_to_write + middle_part_of_path_to_write_pkl
    #print('dir_path_to_write_xlsx=>', dir_path_to_write_xlsx)

    for key, value in dict_of_total_inv_dfs.items():
        #print('key =>', key)

        filename_xlsx = []
        filename_xlsx.append(key + '_Concat_all_mvos_by_2_digits.xlsx')
        full_file_path_xlsx = dir_path_to_write_xlsx + filename_xlsx
        recovered_path_xlsx = Path(*full_file_path_xlsx)

        filename_odf = []
        filename_odf.append(key + '_Concat_all_mvos_by_2_digits.ods')
        full_file_path_odf = dir_path_to_write_odf + filename_odf
        recovered_path_odf = Path(*full_file_path_odf)

        filename_pkl = []
        filename_pkl.append(key + '_Concat_all_mvos_by_2_digits.pkl')
        full_file_path_pkl = dir_path_to_write_pkl + filename_pkl
        recovered_path_pkl = Path(*full_file_path_pkl)

        cre_dir_path_4_xlsx = posixpath.dirname(recovered_path_xlsx)
        cre_dir_path_4_odf = posixpath.dirname(recovered_path_odf)
        cre_dir_path_4_pkl = posixpath.dirname(recovered_path_pkl)

        if not os.path.exists(cre_dir_path_4_xlsx):
            os.makedirs(cre_dir_path_4_xlsx)
        if not os.path.exists(cre_dir_path_4_odf):
            os.makedirs(cre_dir_path_4_odf)
        if not os.path.exists(cre_dir_path_4_pkl):
            os.makedirs(cre_dir_path_4_pkl)

        # write to native pickle df
        value.to_pickle(recovered_path_pkl)

        # to native excel
        with pd.ExcelWriter(recovered_path_xlsx, mode='w') as writer:
            value.to_excel(
                excel_writer=writer,  # файл, в который будем записывать
                sheet_name=key,  # название листа, на который писать
                index=False,  # записывать ли индекс таблицы
                startrow=0,  # строка, с которой начать запись в целевом файле
                startcol=0  # столбец, с которого начать запись в целевом файле
            )

        # to native openpyxl open office ods

        '''with pd.ExcelWriter(recovered_path_odf, engine='odf', mode='w') as writer:
            value.to_excel(
                excel_writer=writer,  # файл, в который будем записывать
                sheet_name=key,  # название листа, на который писать
                index=False,  # записывать ли индекс таблицы
                startrow=0,  # строка, с которой начать запись в целевом файле
                startcol=0  # столбец, с которого начать запись в целевом файле
            )'''



    return None


'''  
 
    # print('cre_dir_path_4_xlsx =>', cre_dir_path_4_xlsx)
    # print('cre_dir_path_4_odf =>', cre_dir_path_4_odf)
    print('cre_dir_path_4_pkl =>', cre_dir_path_4_pkl)
'''