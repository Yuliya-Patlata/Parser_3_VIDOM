import pandas as pd

from reader_inv_10_11_18_xlsx import *
def obs_range_splitter_osn_zasoby(df, filename):
    filename = filename
    if filename[0:2]=='11':
        df = obs_group_inv_no_11(df)
    elif filename[0:2]=='10':
        df = obs_inv_no_range_splitter_10(df)
    else :
        df = df
    return df


def obs_group_inv_no_11(df):
    '''
    Приймає на вхід univ_obs_df у яких перші 2  цифри назви файлу 11 ( тобто 1113  1114 ітд)
    :return: df заповнює колонку inv_no вставляючи рядки де inv_no_range є діапазоном вказаним через тире і
    #потім в додатковому функціоналі ще буде обчислювати є inv_no_psc в цьому діапазоні
    '''
    df['inv_no'] = df['inv_no_range'].apply(lambda x: x[0:10])
    return df.round({'vartist_1':2})

#transformed_11 = group_inv_no_11(df)
#print('transformed_11 =>\n', transformed_11)

def obs_inv_no_range_splitter_10(df):
    '''
    :param df: Приймає на вхід univ_obs_df у яких перші 2 цифри назви файлу 10 ( тобто 1013  1014 1016 ітд)
    :return: df заповнює колонку inv_no вставляючи рядки де inv_no_range є діапазоном вказаним через тире і  обчислює inv_no в цьому діапазоні
    '''
    # unified_df['inv_no'] = unified_df['inv_no_range'].apply(lambda x: x.split('-')[0])
    simple_df = df[df['inv_no_range'].apply(lambda x: len(x) == 9)]
    #simple_df['inv_no'] = simple_df['inv_no_range'].copy()
    simple_df.loc[:,'inv_no'] = simple_df['inv_no_range']

    range_df = df[df['inv_no_range'].apply(lambda x: len(x) > 9 )]
    range_lst_dict = range_df.to_dict('records')
    simplified_lst_dict = []
    for row in range_lst_dict:
        iter_depth = int(row.get('zal_kilk'))
        iter_start = int(row.get('inv_no_range').split('-')[0])
        #iter_start = int(row.get('inv_no_range')[0:10])
        #print(iter_depth, iter_start)
        new_row = row.copy()
        new_row['zal_sum'] = new_row['vartist_1']
        part = []
        for i in range(0,iter_depth):
            new_row['inv_no'] = str(iter_start + i)
            #print(f'new_row \t\t\t{i}=>\t, new_row, '\n')
            part.append(new_row)
            #print(f'part[{i}]', part[i])
            line = part[i].copy()
            simplified_lst_dict.append(line)
        #print('part=>', part)# затираются значения получаемые в цикле  из-за ссылки на объект вместо  глубокого   копрования

    #print('len(simplified_lst_dict)=>', len(simplified_lst_dict))
    #print('simplified_lst_dict=>', simplified_lst_dict)

    simplified_df = pd.DataFrame(simplified_lst_dict)
    #pprint.pp(simplified_df)
    total_df = pd.concat([simplified_df, simple_df], axis=0)
    #pprint.pp(total_df)
    return total_df.round({'vartist_1':2})

#splitted_df = range_splitter_11(df)
#print(df)
