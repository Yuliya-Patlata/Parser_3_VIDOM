import pandas as pd

from reader_inv_10_11_18_xlsx import *


def inv_no_range_splitter_10(df):
    # unified_df['inv_no'] = unified_df['inv_no_range'].apply(lambda x: x.split('-')[0])
    simple_df = df[df['inv_no_range'].apply(lambda x: len(x) == 9)]
    #simple_df['inv_no'] = simple_df['inv_no_range'].copy()
    simple_df.loc[:,'inv_no'] = simple_df['inv_no_range']

    range_df = df[df['inv_no_range'].apply(lambda x: len(x) > 9 )]
    range_lst_dict = range_df.to_dict('records')
    simplified_lst_dict = []
    for row in range_lst_dict:
        iter_depth = int(row.get('kilkist'))
        iter_start = int(row.get('inv_no_range').split('-')[0])
        #iter_start = int(row.get('inv_no_range')[0:10])
        #print(iter_depth, iter_start)
        new_row = row.copy()
        new_row['zag_vartist'] = new_row['vartist_1']
        new_row['sum_znos'] = new_row['sum_znos']/new_row['kilkist']
        new_row['bal_vartist'] = new_row['bal_vartist']/new_row['kilkist']

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
    return total_df.round({'vartist_1':2, 'sum_znos':2, 'bal_vartist':2})

#splitted_df = range_splitter_11(df)
#print(df)
