
import pandas as pd
import numpy as np
from pprint import pp
import pathlib
import pickle
import re
from datetime import datetime
import locale
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

#path_to_folder_with_xlsx = '/home/dream/PycharmProjects/TEST_DATA/oborotky_cxd'


def raw_obs_xlsx_reader(files_attrs_lst):
    '''
    Получает  на вход список списков с  путями  к файлам прочитанным в  директории,
    возвращает список сырых датафреймов созданных из этих  файлов и их параметры
    :param df_list:
    :return:
    '''

    dtype_mapping = {
                    'nazva_with_code': 'object',
                    'od_vymiru': 'U15',
                    'zal_poch_kilk':'float32',
                    'zal_poch_sum': 'float32',
                    'pryb_kilk':'float32',
                    'pryb_suma': 'float32',
                    'vytr_kilk': 'float32',
                    'vytr_sum':'float32',
                    'zal_kilk':'float32',
                    'zal_sum':'float32',
                    }


    clean_obs_df = pd.DataFrame({col:pd.Series(dtype=dtype) for col, dtype in dtype_mapping.items()})
    #print('clean_obs_df.info()=>\n',clean_obs_df.info())
    #print('clean_obs_df.dtypes=>\n', clean_obs_df.dtypes)

    obs_xlsx_file_path = files_attrs_lst[1]
    # print('obs_xlsx_file_path -->', obs_xlsx_file_path)
    raw_obs_df = pd.read_excel(obs_xlsx_file_path,
                            engine='openpyxl',
                            sheet_name=0,
                            skiprows=6,
                            header = None,
                            names=list(dtype_mapping.keys()),
                            )
    for col in clean_obs_df.columns:
        #print(f'col={col}')
        if clean_obs_df[col].dtype == 'float32':
            clean_obs_df[col] = pd.to_numeric(raw_obs_df[col], errors='coerce').astype('float32')
        else: clean_obs_df[col] = raw_obs_df[col].apply(lambda x: x if pd.notna(x) else np.nan)

    # Удалим последнюю строку " ЗАГАЛОМ:"
    clean_obs_df = clean_obs_df[:-1]
    return clean_obs_df

def columns_to_add(files_attrs_lst):

    obs_xlsx_file_path = files_attrs_lst[1]
    # Збережемо назву рахунку, значення укр ПІБ МВО,  часового періоду оборотки в  окремі списки,
    # щоб потім у ф-ї univ_obs_col_prep  вставити їх в створені  там колонки

    nazva_rahunku_read = pd.read_excel(obs_xlsx_file_path, nrows=1)
    nazva_rahunku_dtype = str(nazva_rahunku_read[nazva_rahunku_read.columns[0]])
    nazva_rahunku = nazva_rahunku_dtype[121:(len(nazva_rahunku_dtype) - 15)]
    #print('nazva_rahunku =>', nazva_rahunku)
    no_rahunku = nazva_rahunku.split('-')[0].lstrip()
    #print('no_rahunku=>', no_rahunku)
    dirty_period = pd.read_excel(obs_xlsx_file_path, nrows=1, skiprows=2)
    #print('dirty_period -->\n', dirty_period, '\n')
    period_column = dirty_period.columns[0]
    #print('period_column=>', period_column )
    period_dtype = str(dirty_period[dirty_period.columns[0]])
    clean_period = period_dtype[34:53]
    # print('clean_period -->\n', clean_period, '\n')
    start_end = clean_period.split('-')
    #print('start_end -->', start_end )
    start_date = str(start_end[0]).rstrip().strip()
    end_date = str(start_end[1]).rstrip().strip()

    #locale.setlocale(locale.LC_TIME, 'uk_UA.UTF-8') # for linux
    #locale.setlocale(locale.LC_TIME, 'Ukrainian_Ukraine') # for windows

    start_date_conv = datetime.strptime(start_date, '%d.%m.%y')
    end_date_conv = datetime.strptime(end_date, '%d.%m.%y')
    #print('start_date_conv=>', start_date_conv)
    #print('type(start_date_conv)=>', type(start_date_conv))
    #print('end_date_conv=>', end_date_conv)

    dirty_mvo_card = pd.read_excel(obs_xlsx_file_path, nrows=1, skiprows=5, header = None)
    #print('dirty_mvo_card =>\n', dirty_mvo_card )
    #print('type(dirty_mvo_card)=>', type(dirty_mvo_card))

    dirty_mvo_card_dtype = str(dirty_mvo_card[dirty_mvo_card.columns[0]])
    # print('len(dirty_mvo_card_dtype) -->', len(dirty_mvo_card_dtype))
    # for num in range(len(dirty_mvo_card_dtype)):
    # print(f'{num} -->{dirty_mvo_card_dtype[num]}')
    spl_mvo_card = dirty_mvo_card_dtype.split(',')
    #print('spl_mvo_card=>', spl_mvo_card)

    mvo_fullname_ukr = spl_mvo_card[0]
    mvo_fullname_ukr = re.sub('0',' ', mvo_fullname_ukr).strip()

    o_br_ind = mvo_fullname_ukr.find('(')
    c_br_ind = mvo_fullname_ukr.find(')')
    dilnytsia_mvo_ukr = mvo_fullname_ukr[o_br_ind+1: c_br_ind]

    mvo_fullname_ukr =  mvo_fullname_ukr if o_br_ind==-1 else mvo_fullname_ukr[0:o_br_ind]
    #print('mvo_fullname_ukr -->', mvo_fullname_ukr)
    mvo_pib_ukr = f'{ mvo_fullname_ukr.split(" ")[0] }' + ' ' + f'{ mvo_fullname_ukr.split(" ")[1][0]}' + "." + f'{ mvo_fullname_ukr.split(" ")[2][0]}' + "."
    #print('mvo_pib_ukr=>', mvo_pib_ukr)

    if dilnytsia_mvo_ukr[0:5] == mvo_fullname_ukr[0:5]: dilnytsia_mvo_ukr = ''
    #print('dilnytsia_mvo_ukr=>', dilnytsia_mvo_ukr)

    col_values_dict = { 'no_rahunku': no_rahunku,
                        'mvo_fullname_ukr': mvo_fullname_ukr,
                        'mvo_pib_ukr': mvo_pib_ukr,
                        'dilnytsia_mvo_ukr': dilnytsia_mvo_ukr,
                        'p_start_date': start_date_conv,
                        'p_end_date': end_date_conv,
                        'nazva_rahunku': nazva_rahunku,
                        }
    #print('col_values_dict=>', col_values_dict)
    return   col_values_dict
'''
def export_to_xlsx(df_list, list_of_normalized_dfs):

    for i in range(len(list_of_normalized_dfs)):
        name_of_xlsx_file = 'df_' + df_list[i][2] +'.xlsx'
        path_to_res_xlsx_file = '/home/dream/PycharmProjects/TEST_DATA/WRITE_FILES/' +  name_of_xlsx_file
        #path_to_res_xlsx_file = '/home/dream/PycharmProjects/TEST_DATA/WRITE_FILES/df_' + str(i) + '.xlsx'

        with pd.ExcelWriter(
        path_to_res_xlsx_file,  # путь к файлу
        mode='w'  # открываем на запись, поведение то же, что и у функции open
        ) as writer: list_of_normalized_dfs[i].to_excel(writer)


def export_to_csv(df_list, list_of_normalized_dfs):

    for i in range(len(list_of_normalized_dfs)):
        #print('df_list[i][2] -->', df_list[i][2])
        #path_to_res_csv_file = df_list[i][0]

        name_of_csv_file = 'df_' + df_list[i][2] + '.csv'
        path_to_res_csv_file = '/home/dream/PycharmProjects/TEST_DATA/WRITE_FILES/' + name_of_csv_file

        list_of_normalized_dfs[i].to_csv(
            path_to_res_csv_file,  # путь к файлу, в который делаем запись
            sep='~',  # разделитель колонок
            header=True,  # записывать ли имена колонок в файл (True - записывать, False - нет)
            index=False,  # записывать ли индекс в файл (True - записывать, False - нет)
        )

def write_to_pickle(df_list, list_of_normalized_dfs):

    for i in range(len(list_of_normalized_dfs)):
        name_of_pkl_file = 'df_' + df_list[i][2] +'.pkl'
        path_to_res_pkl_file = '/home/dream/PycharmProjects/TEST_DATA/WRITE_FILES/' +  name_of_pkl_file
        #path_to_res_xlsx_file = '/home/dream/PycharmProjects/TEST_DATA/WRITE_FILES/df_' + str(i) + '.xlsx'
        list_of_normalized_dfs[i].to_pickle(path_to_res_pkl_file)

'''



