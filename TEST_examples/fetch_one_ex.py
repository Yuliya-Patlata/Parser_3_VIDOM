from sqlalchemy import create_engine, text

# Create engine
engine = create_engine('postgresql+psycopg2://lucid:1@localhost:5432/ulbp')

# Query
query = text('SELECT * FROM obs_src_10__10_02_25 WHERE LENGTH(TRIM(inv_no_range)) > 9;')

#1) as a tuple fetchone() Execute and fetch one row
with engine.connect() as connection:
    result = connection.execute(query)
    row = result.fetchone()  # Fetch just one row
    rows = result.fetchall()

if rows:
    print(rows)  # Outputs as a tuple
else:
    print("No matching rows found.")

#2)As dict fetchone()
with engine.connect() as connection:
    res = connection.execute(query)
    one_row_dict = dict(res.mappings().fetchone())
    print('one_row_dict=>',one_row_dict)

#3 In SQLAlchemy, the connection itself acts
# as a cursor, and we can iterate row by row using fetchone() inside a loop.
#Example: Fetch Rows One by One
print('Example: Fetch Rows One by One')

with engine.connect() as conn:
    res = conn.execute(query)
    while (row:=res.mappings().fetchone()) is not None:
        print(dict(row))

#A1005 – Skipping NULL Rows in Python
#Solution: Check for Non-NULL Values in Python


# Create database engine
engine = create_engine('postgresql+psycopg2://lucid:1@localhost:5432/ulbp')

# Query to fetch all rows
query = text('SELECT * FROM obs_src_10__10_02_25;')

with engine.connect() as conn:
    result = conn.execute(query)

    for row in result.mappings().fetchall():  # Convert each row to a dictionary
        row_dict = dict(row)

        # Check if all values (except 'id') are NULL
        non_null_values = [v for k, v in row_dict.items() if k != 'id' and v is not None]

        if non_null_values:  # Only print rows that have at least one non-null value
            print(row_dict)






