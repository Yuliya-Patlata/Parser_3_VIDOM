import pandas as pd
from sqlalchemy import create_engine, text
from get_answers_from_input import choose_test_or_real_db

#engine = choose_test_or_real_db().get('db_engine')
def filter_lst_of_table_names(engine, first_letters_of_tab_names_to_filter):
    # Читаємо в  список назви всіх  таблиць бд
    filtering_str = first_letters_of_tab_names_to_filter
    db_tabs_lst_query = text("""SELECT table_name FROM information_schema.tables
     WHERE table_schema = 'public' AND table_type = 'BASE TABLE' ;""")
    with engine.connect() as conn:
        result = conn.execute(db_tabs_lst_query)
        table_names = [row[0] for row in result.fetchall()]
        # print("Tables in public schema:", table_names)
        # вибираємо з загального списку  таблиць  лише потрібні #для джоїна
    filtered_tab_names = []
    for tab_name in table_names:
        if tab_name[0:len(filtering_str)] == filtering_str:
            filtered_tab_names.append(tab_name)

    return filtered_tab_names

def cre_dict_of_dfs(engine, tab_names_lst, ):
    dict_of_dfs ={}
    for tab_name in tab_names_lst:
        with engine.connect() as conn:
            common_query = text(f'SELECT * FROM {tab_name};')
            result = conn.execute( common_query)
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
            print(f'{tab_name} Raw result =>\n', df)
            dict_of_dfs.__setitem__(tab_name, df)
    return dict_of_dfs


