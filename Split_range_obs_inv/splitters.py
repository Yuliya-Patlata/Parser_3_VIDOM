from sqlalchemy import create_engine, text
from TEST_examples.inv_range_splitter_10 import *

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

def inv_inv_no_range_splitter_10(df):
    '''
    В 10 інвентарках щепить діапазон inv_no_range,
    щоб був  поштучний  облік inv_no придатний
    для  merge по inv_no з 10 оборотками
    :param df:
    :return:
    '''
    # unified_df['inv_no'] = unified_df['inv_no_range'].apply(lambda x: x.split('-')[0])
    simple_df = df[df['inv_no_range'].apply(lambda x: len(x) == 9)]
    #simple_df['inv_no'] = simple_df['inv_no_range'].copy()
    simple_df.loc[:,'inv_no'] = simple_df['inv_no_range']

    range_df = df[df['inv_no_range'].apply(lambda x: len(x) > 9 )]
    range_lst_dict = range_df.to_dict('records')
    simplified_lst_dict = []
    for row in range_lst_dict:
        iter_depth = int(row.get('kilkist'))# zal_kilk
        iter_start = int(row.get('inv_no_range').split('-')[0])
        #iter_start = int(row.get('inv_no_range')[0:10])
        #print(iter_depth, iter_start)
        new_row = row.copy()
        new_row['zag_vartist'] = new_row['vartist_1']#zal_sum
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


def inv_range_splitter_10_11(db_con_str, sql_query):
    engine = create_engine(db_con_str)
    query = text(sql_query)
    with engine.connect() as con:
        result = con.execute(query)
        #rows = result.fetchall()
        #print('type(rows)=>', type(rows))
        lst_rows_of_dicts = [dict(row) for row in result.mappings().fetchall()]
        df = pd.DataFrame(lst_rows_of_dicts)
    return  inv_inv_no_range_splitter_10(df)




