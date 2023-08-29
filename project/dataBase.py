import pandas as pd
import sqlite3

# Import data into sqlite database
cityIndex=pd.read_excel('static/CostIndex.xlsx', header=0)

db_conn=sqlite3.connect('cost.db')
cursor=db_conn.cursor()
cursor.execute(
    """
    CREATE TABLE cityIndex (
    state TEXT NOT NULL,
    city TEXT NOT NULL,
    Material REAL,
    Installation REAL,
    Average REAL
    )
    """
)
cityIndex.to_sql('cityIndex', db_conn)

db_conn.commit()
db_conn.close()