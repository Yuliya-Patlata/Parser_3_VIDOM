import pandas as pd
import numpy as np
from copy import deepcopy
from remove_invisible_symbols_from_text import clean_text_columns


pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
def cre_univ_obs_df(clean_obs_df, en_pib_dilnutsia_lst, col_dict):
    univ_obs_df = deepcopy(clean_obs_df)

    added_col_values_dict = col_dict

    # создадим новые столбцы с одним  и  тем  же  значением для  всех   строк

    univ_obs_df['mvo_pib_en'] = en_pib_dilnutsia_lst[0]
    univ_obs_df['dilnytsia_mvo_en'] = en_pib_dilnutsia_lst[1]


    univ_obs_df['dilnytsia_mvo_ukr'] = added_col_values_dict['dilnytsia_mvo_ukr']
    univ_obs_df['mvo_fullname_ukr'] = added_col_values_dict['mvo_fullname_ukr']
    univ_obs_df['mvo_pib_ukr'] = added_col_values_dict['mvo_pib_ukr']
    univ_obs_df['p_start_date'] = added_col_values_dict['p_start_date']
    univ_obs_df['p_end_date'] = added_col_values_dict['p_end_date']
    univ_obs_df['nazva_without_code'] = univ_obs_df['nazva_with_code'].apply(parser_nazva_without_code)
    univ_obs_df['sp_status'] = univ_obs_df['zal_kilk'].apply(lambda x: 'числиться' if x>0 else 'списано')
    univ_obs_df['spl_inv_no'] = np.nan

    univ_obs_df['category'] = 'не вказано'

    univ_obs_df.insert(
        loc=0,
        column='no_rahunku',
        value = added_col_values_dict['no_rahunku'].strip()
    )

    univ_obs_df.insert(
        loc=1,
        column='inv_no_range',
        value = univ_obs_df['nazva_with_code'].apply(inv_no_range_parser)
    )

    univ_obs_df.insert(
        loc=2,
        column='inv_no',
        value= univ_obs_df['inv_no_range'].apply(lambda x : str(x)[0:9] if pd.notna(x) else 'missing_inv_no')
    )

    univ_obs_df.insert(
        loc=3,
        column='psc_inv_no',
        value = '_of_'
    )

    # ствoримо обислювану колонку vartist_1 (price_of_unit)
    univ_obs_df.insert(
        loc=14,
        column='vartist_1',
        value = univ_obs_df['zal_sum']/univ_obs_df['zal_kilk']
    )
    univ_obs_df['f_len'] = univ_obs_df['no_rahunku'].apply(lambda x: len(x))
    univ_obs_df['split_flag'] = univ_obs_df['no_rahunku'].apply(lambda x: False if x in ['1816','1514'] else True)
    #univ_obs_df['split_flag'] = univ_obs_df['no_rahunku'].apply(lambda x: x not in ['1816', '1514'])# але чекбокси неправильно відображаються в бд
    #print('univ_obs_df.columns=', univ_obs_df.columns)
    #print('univ_obs_df.columns.dtypes=', univ_obs_df.info())
    univ_obs_df = clean_text_columns(univ_obs_df)
    return univ_obs_df.round({'vartist_1':2,'zal_poch_sum':2,'zal_sum':2 })


def inv_no_range_parser(nazva_with_code):
    if nazva_with_code[-12] == '-':
        return nazva_with_code[-22:-1]

    s_plitted = nazva_with_code.split("[")
    # print('splitted_s', s_plitted)

    if s_plitted[-1][0] == 'к':
        ss_plitted = s_plitted[-1].split(" ")
        # print('ss_plitted', ss_plitted)
        return ss_plitted[-1][:-1]
    else:
        return s_plitted[-1][:-1]

def parser_nazva_without_code(nazva_with_code):
    s_plitted = nazva_with_code.split("[")
    return s_plitted[0]

