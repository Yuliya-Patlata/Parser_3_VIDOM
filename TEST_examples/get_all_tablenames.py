from sqlalchemy import create_engine, text
from sqlalchemy.dialects import postgresql

engine = create_engine('postgresql+psycopg2://lucid:1@localhost:5432/ula_test')
query = text("""SELECT table_name FROM information_schema.tables
 WHERE table_schema = 'public' AND table_type = 'BASE TABLE' ;""")
with engine.connect() as conn:
    result = conn.execute(query)
    table_names = [ row[0] for row in result.fetchall()]
    print("Tables in public schema:", table_names)
for item in table_names:
    print(item)


table_name= "obs_src_11__10_02_25"
col_names_query = text("""SELECT column_name, data_type FROM information_schema.columns WHERE table_schema = 'public' AND table_name = :table_name;""")
with engine.connect() as conn:
    result = conn.execute( col_names_query,{'table_name': table_name })
    rows = result.fetchall()
    print('Raw result =>', rows)

    #columns = [(row[0], row[1]) for row in result.fetchall()]
    #print(f"Columns in {table_name}:")

'''for col_name, col_type in columns:
    print(f"- {col_name} ({col_type})")'''