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

def writers_to_separate_files(univ_df, file_attrs_lst ):
    df_to_write = univ_df
    file_attrs_lst = file_attrs_lst
    #print('file_attrs_lst=>', file_attrs_lst)
    filename_without_ext = file_attrs_lst[-2]
    path_str = file_attrs_lst[1]
    directory = posixpath.dirname(path_str)
    #print('directory= posixpath.dirname(path_str) =>', directory)
    #print('filename_without_ext =>', filename_without_ext)
    p = pathlib.PurePath(directory)
    list_of_parts = list(p.parts)

    #print('list_of_parts =>',list_of_parts)
    lst_split_index = list_of_parts.index('READ_FILES')
    first_part_of_path = list_of_parts[0:lst_split_index]
    #print('first_part_of_path =>',first_part_of_path)
    last_part_of_path = list_of_parts[lst_split_index + 1:]
    #print('last_part_of_path =>', last_part_of_path)
    middle_part_pf_path_xlsx = ['WRITE_FILES','ZAVDANNIA_TEST', 'INV_OPYSY','SEPARATED_BY_MVO','XLSX']
    middle_part_pf_path_odf = ['WRITE_FILES', 'ZAVDANNIA_TEST', 'INV_OPYSY','SEPARATED_BY_MVO','ODF']
    middle_part_pf_path_pkl = ['WRITE_FILES','ZAVDANNIA_TEST','INV_OPYSY','SEPARATED_BY_MVO', 'PKL']

    filename_xlsx =[]
    filename_xlsx.append(filename_without_ext[:] + '.xlsx')
    #print('filename_xlsx =>', filename_xlsx)
    filename_odf = []
    filename_odf.append(filename_without_ext[:] + '.ods')
    filename_pkl = []
    filename_pkl.append(filename_without_ext[:] + '.pkl')

    full_path_xlsx = first_part_of_path + middle_part_pf_path_xlsx + last_part_of_path + filename_xlsx
    full_path_odf = first_part_of_path + middle_part_pf_path_odf + last_part_of_path + filename_odf
    full_path_pkl = first_part_of_path + middle_part_pf_path_pkl + last_part_of_path + filename_pkl

    recovered_path_xlsx = Path(*full_path_xlsx )
    recovered_path_odf = Path(*full_path_odf)
    recovered_path_pkl = Path(*full_path_pkl)
    #print('recovered_path_xlsx =>', recovered_path_xlsx)
    #print('recovered_path_pkl =>', recovered_path_pkl)

    cre_dir_path_4_xlsx = posixpath.dirname(recovered_path_xlsx)
    cre_dir_path_4_odf = posixpath.dirname(recovered_path_odf)
    cre_dir_path_4_pkl = posixpath.dirname(recovered_path_pkl)
    #print('cre_dir_path_4_xlsx =>', cre_dir_path_4_xlsx)
    #print('cre_dir_path_4_odf =>', cre_dir_path_4_odf)
    #print('cre_dir_path_4_pkl =>', cre_dir_path_4_pkl)
    if not os.path.exists(cre_dir_path_4_xlsx):
        os.makedirs(cre_dir_path_4_xlsx)
    if not os.path.exists(cre_dir_path_4_odf):
        os.makedirs(cre_dir_path_4_odf)
    if not os.path.exists(cre_dir_path_4_pkl):
        os.makedirs(cre_dir_path_4_pkl)

    # to native pickle df
    df_to_write.to_pickle(recovered_path_pkl)

    #to native excel
    with pd.ExcelWriter(recovered_path_xlsx, mode='w') as writer:
        df_to_write.to_excel(
                excel_writer=writer,  # файл, в который будем записывать
                sheet_name= filename_without_ext,  # название листа, на который писать
                index=False,  # записывать ли индекс таблицы
                startrow=0,  # строка, с которой начать запись в целевом файле
                startcol=0  # столбец, с которого начать запись в целевом файле
            )

    '''# to native openpyxl open office ods
    with pd.ExcelWriter(recovered_path_odf,engine='odf', mode='w') as writer:
        df_to_write.to_excel(
                excel_writer=writer,  # файл, в который будем записывать
                sheet_name= filename_without_ext,  # название листа, на который писать
                index=False,  # записывать ли индекс таблицы
                startrow=0,  # строка, с которой начать запись в целевом файле
                startcol=0  # столбец, с которого начать запись в целевом файле
            )'''


    return None


