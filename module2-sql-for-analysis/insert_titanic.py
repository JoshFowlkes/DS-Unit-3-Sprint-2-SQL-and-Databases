import psycopg2
import sqlite3
import pandas as pd 

# bringing in the dataset
titanic_df = pd.read_csv('titanic.csv')
titanic_df.columns = ['Survived', 'Pclass', 'Name', 'Sex', 'Age',
              'Siblings_Spouses_Aboard', 'Parents_Children_Aboard', 'Fare']
titanic_df['Name'] = titanic_df['Name'].str.replace("'", "")

# setting engine and converting df to sql
sl_conn = sqlite3.connect('titanic_table')
titanic_df.to_sql('titanic_table', con=sl_conn, if_exists='replace')
sl_curs = sl_conn.cursor()


# dont commit  password, 
dbname = ''
user = ''
password = '' # DONT COMMIT THIS
host = ''

pg_conn = psycopg2.connect(dbname = dbname, user = user,
                        password = password, host = host)

pg_curs = pg_conn.cursor()


# drop titanic table if it already exists 
pg_curs.execute('DROP TABLE IF EXISTS titanic_table')


# with that check complete, we have EXTRACT (from ETL) done, now on to TRANSFORM
create_titanic_table = """
CREATE TABLE titanic_table (
    Survived INT,
    Pclass INT,
    Name TEXT,
    Sex TEXT,
    Age REAL,
    Siblings_Spouses_Aboard	INT,
    Parents_Children_Aboard	INT,
    Fare REAL
);
"""
# actually executing the order to create the table
pg_curs.execute(create_titanic_table)

# Get data from sqlite table
persons = sl_curs.execute('SELECT * FROM titanic_table').fetchall()



# building an insert for one entry, to model how I'll build my loop
insert_one = """
INSERT INTO titanic_table
(Survived, Pclass, Name, Sex, Age, Siblings_Spouses_Aboard, Parents_Children_Aboard, Fare )
VALUES """ + str(persons[1:]) + ';'


# using for loop to load all the entries at once
for person in persons:
    insert_person = """
    INSERT INTO titanic_table
    (Name, Survived, Pclass, Sex, Age, Siblings_Spouses_Aboard, Parents_Children_Aboard, Fare)
    VALUES """ + str(person[1:])
    print(insert_person)
# this checks within the py file
pg_curs.execute('SELECT * FROM titanic_table')
pg_curs.fetchall()



# to actually commit to elephantsql
pg_curs.close()
pg_conn.commit()
""" From here, should be on Elephant SQL, go check there """



# to check programmatically
pg_curs = pg_conn.cursor()
pg_curs.execute('SELECT * FROM titanic_table;')
pg_persons = pg_curs.fetchall()

assert(persons[0] == pg_persons[0])

""" WIth that, Boom boom! Titanic data should be on elephant SQL, from here, can mess with query's and such """

