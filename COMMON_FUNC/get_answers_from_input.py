
from sqlalchemy import create_engine, text

def choose_test_or_real_db():
    answer = input('For working with Test_db or Real_db input letter T or RDB :')
    try:
        if answer not in {'T', 'RDB'}:
            raise ValueError('YOU HAVE ENTERED UNACCEPTABLE VALUE !!!')
    except ValueError as e:
        print(f'Error:{e}')
    else:
        print(f'Your answer - "{answer}" is acceptable')
        if answer == "T":
            # Dirs for short TEST tasks
            READ_START_of_nested_dirs = "/home/dream/PycharmProjects/Parser_3_VIDOM/READ_FILES/ZAVDANNIA_TEST"
            WRITE_START_of_nested_dirs = "/home/dream/PycharmProjects/Parser_3_VIDOM/WRITE_FILES/ZAVDANNIA_TEST"
            engine = create_engine('postgresql+psycopg2://lucid:1@localhost:5432/ula_test')

        elif answer == 'RDB':
            # Dirs for  real  tasks
            READ_START_of_nested_dirs = "/home/dream/PycharmProjects/Parser_3_VIDOM/READ_FILES/ZAVDANNIA"
            WRITE_START_of_nested_dirs = "/home/dream/PycharmProjects/Parser_3_VIDOM/WRITE_FILES/ZAVDANNIA"
            engine = create_engine('postgresql+psycopg2://lucid:1@localhost:5432/ula_real')

        start_params_dict = { 'read_start_path': READ_START_of_nested_dirs,
             'write_start_path': WRITE_START_of_nested_dirs,
             'db_engine': engine }

        return start_params_dict

#start_params_dict = choose_test_or_real_db()
#print(start_params_dict)
