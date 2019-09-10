import psycopg2
import sqlite3
import pandas as pd 
from sqlalchemy import create_engine


# dont commit  password, 
dbname = 'xftzfimi'
user = 'xftzfimi'
password = 'hv5bMWTZcnfmQYBVvTa1BDOz1KAOnrhR' # DONT COMMIT THIS
host = 'salt.db.elephantsql.com'

pg_conn = psycopg2.connect(dbname = dbname, user = user,
                        password = password, host = host)

pg_curs = pg_conn.cursor()

# Use these just to test out the connection to the Elephant SQL database
pg_curs.execute('SELECT * FROM charactercreator_character')
pg_curs.fetchall()

# bringing in the dataset
titanic_df = pd.read_csv('titanic.csv')

# pandas to sql
engine = create_engine('postgresql+psycopg2://'+user+':'+password+'@'+host+'/'+dbname)
titanic_df.to_sql('titanic', if_exists='replace', con=engine)

# assigning SQL connection and cursor
s1_conn = sqlite3.connect('titanic')
s1_curs = s1_conn.cursor()

# a quick query to check and see that it all worked
s1_curs.execute('SELECT count(Name) FROM titanic ').fetchall()

persons = s1_curs.execute('SELECT * FROM titanic').fetchall()

# with that check complete, we have EXTRACT (from ETL) done, now on to TRANSFORM
create_titanic_table = """
CREATE TABLE titanic_table (
   Name SERIAL PRIMARY KEY,
    Survived INT,
    Pclass INT,
    Sex VARBINARY(10),
    Age INT,
    Siblings/Spouses Aboard	INT,
    Parents/Children Aboard	INT,
    Fare FLOAT
)
"""
# actually executing the order to create the table
pg_curs.execute(create_titanic_table)

# building an insert for one entry, to model how I'll build my loop
insert_one = """
INSERT INTO titanic_table
(Name, Survived, Pclass, Sex, Age, Siblings/Spouses Aboard, Parents/Children Aboard, Fare )
VALUES """ + str(persons[1:]) + ';'

# using for loop to load all the entries at once
for person in persons:
    insert_person = """
    INSERT INTO titanic_table
    (Name, Survived, Pclass, Sex, Age, Siblings/Spouses Aboard, Parents/Children Aboard, Fare)
    VALUES """ + str(person[1:])
    print(insert_person)
    pg_curs.execute(insert_person)

# this checks within the py file
pg_curs.execute('SELECT * FROM titanic_table')
pg_curs.fetchall()

# to actually commit to elephantsql
pg_curs.close()
#pg_conn.commit()
""" From here, should be on Elephant SQL, go check there """

# to check programmatically
pg_curs = pg_conn.cursor()
pg_curs.execute('SELECT * FROM titanic_table;')
pg_persons = pg_curs.fetchall()

assert(persons[0] == pg_persons[0])

""" WIth that, Boom boom! Titanic data should be on elephant SQL, from here, can mess with query's and such """