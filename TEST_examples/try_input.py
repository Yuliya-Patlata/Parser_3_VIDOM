
def choose_test_or_real_db():
    answer = input('For working with Test_db or Real_db input letter T or RDB :')
    try:
        if answer not in {'T', 'RDB'}:
            raise ValueError('YOU HAVE ENTERED UNACCEPTABLE VALUE !!!')
    except ValueError as e:
            print(f'Error:{e}')
    else:
        print( f"'{answer}' is acceptable" )

choose_test_or_real_db()