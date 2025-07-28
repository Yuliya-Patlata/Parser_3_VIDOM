import numpy as np
import pandas as pd
from remove_invisible_symbols_from_text import clean_text_columns

def convert_to_universal_df(dd_mm_yy, trimmed_df, file_description):

    file_name = file_description[2]
    unified_df = pd.DataFrame( data=[], columns=[  'dd_mm_yy',
                                                   'mvo_pib_en',
                                                   'dilnytsia_mvo_en',
                                                   'por_no',
                                                   'sub_rah',
                                                   'nazva_desc',
                                                   'rik',
                                                   'inv_no_range',
                                                   'inv_no',
                                                   'zavod_no',
                                                   'passport_no',
                                                   'od_vymiru',
                                                   'kilkist',
                                                   'vartist_1',
                                                   'zag_vartist',
                                                   'sum_znos',
                                                   'bal_vartist',
                                                   'termin_vyk',
                                                   'prymitka'])
    #print('unified_df.shape=>',unified_df.shape)
    #print('trimmed_df.shape=>', trimmed_df.shape)
    # print('file_name =',file_name)
    #print('file_name[0:2]=>', file_name[0:2])
    trimmed_df = clean_text_columns(trimmed_df)
    if file_name[0:2] == '11' or file_name[0:2] == '10':
        #print('select 10 like =')
        unified_df[['por_no','nazva_desc','rik','inv_no_range','zavod_no','passport_no','od_vymiru','kilkist','zag_vartist','sum_znos', 'bal_vartist', 'termin_vyk','prymitka']
        ] = trimmed_df[['1', '2','3','4','5','6','7','11','12','13','14','15','16']].copy()
        #unified_df['sub_rah']= unified_df.apply(lambda str(['inv_no_range'])[0:4])
        unified_df['vartist_1'] = unified_df['zag_vartist']/unified_df['kilkist']
        unified_df['spl_inv_no'] = np.nan

        if file_name[0:2] == '11':
            unified_df['inv_no'] = unified_df['inv_no_range'].str.slice(0,9)
            # unified_df['inv_no'] = unified_df['inv_no_range'].str[0:9]

    elif file_name[0:2] == '18' or file_name[0:2] == '15':
        #print('select 18 like =')
        unified_df[['por_no','sub_rah','nazva_desc','inv_no_range','od_vymiru','kilkist','vartist_1','zag_vartist','prymitka']
        ] = trimmed_df[['1', '2','3','4','5','9','10','11','12']].copy()
    #unified_df['inv_no'] = unified_df['inv_no_range'].apply(lambda x: x.split('-')[0])
    #unified_df['inv_no'] = unified_df['inv_no_range'].str.split('-')[0]

    unified_df['dd_mm_yy'] = dd_mm_yy
    unified_df['mvo_pib_en'] = file_description[3][0]
    unified_df['dilnytsia_mvo_en'] = file_description[3][1]
    unified_df.insert(9,"nazva_ckey", None, allow_duplicates=True )
    unified_df.loc[:, 'inv_range_kilk'] = unified_df['kilkist']
    #simple_df.loc[:,'inv_no'] = simple_df['inv_no_range'].str[0:9]
    return unified_df