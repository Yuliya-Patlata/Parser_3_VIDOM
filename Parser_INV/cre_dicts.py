import pandas as pd

def cre_dict_of_total_inv_dfs():
    total_10_inv_df = pd.DataFrame()
    total_11_inv_df = pd.DataFrame()
    total_18_inv_df = pd.DataFrame()
    total_15_inv_df = pd.DataFrame()
    total_xx_inv_df = pd.DataFrame()

    dict_of_total_inv_dfs = { '10' :total_10_inv_df,
                              '11' :total_11_inv_df,
                              '18' :total_18_inv_df,
                              '15' :total_15_inv_df,
                              'xx' :total_xx_inv_df,
                              }
    return dict_of_total_inv_dfs


def cre_dict_of_total_obs_dfs():
    total_10_obs_df = pd.DataFrame()
    total_11_obs_df = pd.DataFrame()
    total_18_obs_df = pd.DataFrame()
    total_15_obs_df = pd.DataFrame()
    total_xx_obs_df = pd.DataFrame()

    dict_of_total_obs_dfs = {'10': total_10_obs_df,
                             '11': total_11_obs_df,
                             '18': total_18_obs_df,
                             '15': total_15_obs_df,
                             'xx': total_xx_obs_df,
                             }
    return dict_of_total_obs_dfs