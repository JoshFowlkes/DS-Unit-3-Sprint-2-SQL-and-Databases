import pandas as pd
import sqlite3

conn = sqlite3.connect('buddymove_holidayiq.sqlite3')
curs = conn.cursor()

df = pd.read_csv('buddymove_holidayiq.csv')
df.to_sql('review', conn, if_exists='replace', index_label='id')

query = 'SELECT * FROM review'
df = pd.read_sql(query, conn)
print(df)

query = "SELECT * FROM review"
conn.execute(query)
conn.commit()

query = "SELECT COUNT(*) FROM review"
results = conn.execute(query)
print('Rows:', results.fetchall()[0][0])

query = """SELECT COUNT(*)
FROM review
WHERE (Nature >=100) AND (Shopping >=100)
"""
results - conn.execute(query)
print("More than 100 nature and shopping reviews: ", results.fetchall()[0][0])
