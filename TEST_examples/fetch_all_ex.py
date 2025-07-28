import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.dialects import postgresql

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
engine = create_engine('postgresql+psycopg2://lucid:1@localhost:5432/ulbp')

# Test the connection
with engine.connect() as conn:
    result = conn.execute(text("SELECT version();"))
    #print(result.fetchone())


#query = text("SELECT * FROM inv_src_10__06_11_24 WHERE LENGTH(inv_no_range) > 9;")
query = text("SELECT * FROM inv_src_10__06_11_24 WHERE LENGTH(TRIM(inv_no_range)) > 9;")
# Execute query and fetch results
#If you want the result directly as list of dicts:
with engine.connect() as connection:
    result = connection.execute(query)
    #rows = result.fetchall()
    #print('type(rows)=>', type(rows))
    lst_rows_of_dicts = [dict(row) for row in result.mappings().fetchall()]

df = pd.DataFrame(lst_rows_of_dicts)
print('len(df)=>', len(df))
print(df.head(10))

#If you want the result directly as a DataFrame:
with engine.connect() as connection:
    result = connection.execute(query)
    rows = result.fetchall()
    d_df = pd.DataFrame(rows, columns=result.keys())
    print('type(rows)=>', type(rows))
    print("result.keys()=>", result.keys())
print('d_df=>\n',d_df)

'''
#Print the fetched rows
for line_t in rows:
    print(line_t)

print('lst_rows_of_dicts=>\n')
for line_d in lst_rows_of_dicts:
    print(line_d)
'''
#print('lst_rows_of_dicts=>\n', lst_rows_of_dicts)
#print('************************')


