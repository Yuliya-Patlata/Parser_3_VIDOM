from sqlalchemy import create_engine, text
import pandas as pd
import re
import numpy as np
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

def inv_no_range_splitter_10(df):
    '''
    В 10 інвентарках щепить діапазон inv_no_range,
    щоб був  поштучний  облік inv_no придатний
    для  merge по inv_no з 10 оборотками
    :param df:
    :return:
    '''
    # unified_df['inv_no'] = unified_df['inv_no_range'].apply(lambda x: x.split('-')[0])
    simple_inv_no_df = df[df['inv_no_range'].apply(lambda x: len(x) == 9)]
    #simple_df['inv_no'] = simple_df['inv_no_range'].copy()
    years = ['2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009']
    simple_1016_range_df = df[(df['inv_no_range'].apply(lambda x: len(x) > 9))
        & (df['inv_no_range'].str[0:4] == '1016')
        & (df['rik'].isin(years))]
    simple_df = pd.concat([simple_inv_no_df, simple_1016_range_df], axis=0)
    simple_df.loc[:,'inv_no'] = simple_df['inv_no_range'].str[0:9]
    removed_range = simple_df['inv_no_range'].tolist()
    #print('removed_range=>', removed_range)
    range_df = df[~df['inv_no_range'].isin(removed_range)]
    #print('range_df=>\n', range_df)

    range_lst_dict = range_df.to_dict('records')
    simplified_lst_dict = []# список  словників
    iter_start_pattern = re.compile(r'^\s*(\d+|\d+\s*-\s*\d+)\s*$')
    generated_inv_no_range = 0
    for row in range_lst_dict:
        iter_depth = int(row.get('kilkist'))# zal_kilk
        #iter_start = int(row.get('inv_no_range').split('-')[0])

        literal = row.get('inv_no_range')[0:10]
        #if len(literal) < 9:
        if isinstance(literal,str) and iter_start_pattern.match(literal):
            iter_start = int(row.get('inv_no_range')[0:10])
        else:
            print('invalid literal=', literal, row.get('nazva_desc'), row.get('mvo_pib_en'))
            generated_inv_no_range += 1   #yield f"{counter_of_invalid_literals:09d}"
            row['inv_no_range'] = "00000000"+str(generated_inv_no_range)
            print("row['inv_no_range']=", row['inv_no_range'])
            iter_start = generated_inv_no_range

        #print(iter_depth, iter_start)
        new_row = row.copy()
        new_row['zag_vartist'] = new_row['vartist_1']#zal_sum
        new_row['sum_znos'] = new_row['sum_znos']/new_row['kilkist']
        new_row['bal_vartist'] = new_row['bal_vartist']/new_row['kilkist']
        new_row['kilkist']=1
        part = []
        for i in range(0,iter_depth):
            new_row['inv_no'] = str(iter_start + i)
            #print(f'new_row \t\t\t{i}=>\t, new_row, '\n')
            part.append(new_row)
            #print(f'part[{i}]', part[i])
            # print('part=>', part)# затирались значення отримані в циклі  через ссилку
            # на об'єкет замість  глибокого  копіювання
            line = part[i].copy()
            simplified_lst_dict.append(line)

    #print('len(simplified_lst_dict)=>', len(simplified_lst_dict))
    #print('simplified_lst_dict=>', simplified_lst_dict)

    simplified_df = pd.DataFrame(simplified_lst_dict)
    #pprint.pp(simplified_df)
    total_df = pd.concat([simplified_df, simple_df], axis=0)
    #pprint.pp(total_df)
    total_df = total_df.round({'vartist_1':2, 'sum_znos':2, 'bal_vartist':2})

    return total_df

def inv_10_range_spliter(engine, inv_tab_10_to_split_and_rename ):
    engine = engine
    inv_tab_10 = inv_tab_10_to_split_and_rename
    query=text(f"SELECT * FROM {inv_tab_10};")

    modif_tab_name = 'l0_wrapped_' + inv_tab_10
    drop_if_exist_query = text(f'DROP TABLE IF EXISTS {modif_tab_name}')
    rename_query = text(f'ALTER TABLE {inv_tab_10} RENAME TO {modif_tab_name};')

    with engine.connect() as con:
        result = con.execute(query)
        #rows = result.fetchall()
        #print('type(rows)=>', type(rows))
        lst_rows_of_dicts = [dict(row) for row in result.mappings().fetchall()]
        df = pd.DataFrame(lst_rows_of_dicts)
        con.execute(drop_if_exist_query)
        con.execute(rename_query)
        con.commit()

    print(f"Table renamed from '{inv_tab_10}' to '{modif_tab_name}' successfully.")

    splited_inv_10_df = inv_no_range_splitter_10(df)
    splited_inv_10_df.to_sql(name=inv_tab_10, con=engine, index=False, if_exists='replace')

    return None




