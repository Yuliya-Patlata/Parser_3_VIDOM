import pandas as  pd
import xlrd
import openpyxl
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
#file_path = '/home/dream/PycharmProjects/Parser_INVENTARN/Parser_INV/test.xls'

#path_to_file_str = '/home/dream/PycharmProjects/Parser_INV_OB/READ_FILES/ZAVDANNIA_TEST/RENKAS/ENTOMOLOGICHNYKH//ZVD_1__INV_OPYSY/11_ент.xlsx'

def skip_rows_file_name_parser(file_description):
    file_name = file_description[2]
    #print('file_name =',file_name)
    skip_rows = 0
    #print('file_name[0:2]=>', file_name[0:2])
    if file_name[0:2]=='11'or file_name[0:2] =='10':
        skip_rows=31
        #print('skip_rows=', skip_rows)

    elif file_name[0:2]=='18' or file_name[0:2]=='15':
        skip_rows = 29
        #print('skip_rows=', skip_rows)
    df = pd.read_excel(file_description[1],
        skiprows = skip_rows)
    #print(df)
    return df


#raw_df = skip_rows_file_name_parser(path_to_file_str)
#print('********')
#print('raw_df.info=>', raw_df.info())

def end_trimmer(df):
    trimmed_df = df
    end_index = trimmed_df[
    (trimmed_df['1'] == 'Разом') &
    (trimmed_df['2'] == 'Х') &
    (trimmed_df['3'] == 'Х')
    ].index # .index.values.astype(int)
    #print('end_index=>', end_index)
    #print('type(end_index)=>', type(end_index))
    # розпаковуємо 0 елемент  класу Index([3], dtype='int64')
    end_no = int(end_index[0])
    #print('type(end_no)=>', type(end_no))
    #print('end_no=>', end_no )
    trimmed_df = trimmed_df[(trimmed_df.index < end_no)]
    #print('trimmed_df=>\n', trimmed_df )
    return trimmed_df

#tr_df = end_trimmer(raw_df)





