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
dbname = 'xftzfimi'
user = 'xftzfimi'
password = 'hv5bMWTZcnfmQYBVvTa1BDOz1KAOnrhR' # DONT COMMIT THIS
host = 'salt.db.elephantsql.com'

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

'''-------- QUERIES ---------'''
query = 'SELECT COUNT(*) FROM titanic_table;'
ans = sl_curs.execute(query).fetchall()
print('total count:', ans)


query = 'SELECT COUNT(name) FROM titanic_table GROUP BY Survived'
ans = sl_curs.execute(query).fetchall()
print('Count of people who DID NOT survive', ans[0], 'Did Survive: ', ans[1])

query = 'SELECT COUNT(name) FROM titanic_table WHERE Survived = 1'
ans = sl_curs.execute(query).fetchall()
print('Count of people who DID survive', ans)

query = 'SELECT COUNT(name) FROM titanic_table WHERE Survived = 0'
ans = sl_curs.execute(query).fetchall()
print('Count of people who did not survive',ans)

# Passengers in each class count
query = 'SELECT COUNT(name) FROM titanic_table GROUP BY PClass'
ans = sl_curs.execute(query).fetchall()
print('Count of people Group1', ans[0], 'Group2: ', ans[1], 'Group3:', ans[2])

# How many passengers survived/died within each class?
query = 'SELECT COUNT(name) FROM titanic_table GROUP BY PClass, Survived'
ans = sl_curs.execute(query).fetchall()
print(ans)

#What was the average age of each passenger class?
query = 'SELECT AVG(Age) FROM titanic_table GROUP BY PClass'
ans = sl_curs.execute(query).fetchall()
print('Average age grouped by Passenger Class ',ans)

query = ' SELECT COUNT(Name) FROM titanic_table GROUP BY PClass '
ans = sl_curs.execute(query).fetchall()
print('Count of people, by Passenger Class',ans)

query = 'SELECT COUNT(Name) FROM titanic_table WHERE Survived = 1 GROUP BY PClass'
ans = sl_curs.execute(query).fetchall()
print('Count of people who survived by Passenger Class', ans)

query = 'SELECT COUNT(Name) FROM titanic_table WHERE Survived = 0 GROUP BY PClass'
ans = sl_curs.execute(query).fetchall()
print('Count of people who did NOT survive by Passenger Class', ans)

# DISTINT NAMES
query = 'SELECT COUNT(*) FROM(SELECT DISTINCT Name FROM titanic_table)'
ans = sl_curs.execute(query).fetchall()
print('Count of Distinct Names', ans)

# How many siblings/spouses aboard on average, by passenger class? By survival?
query = 'SELECT AVG(Siblings_Spouses_Aboard) FROM titanic_table GROUP BY PClass, Survived'
ans = sl_curs.execute(query).fetchall()
print(ans)

query = 'SELECT AVG(Parents_Children_Aboard) FROM titanic_table GROUP BY PClass, Survived'
ans = sl_curs.execute(query).fetchall()
print(ans)

query  = 'SELECT AVG(Fare) FROM titanic_table'
ans = sl_curs.execute(query).fetchall()
print(ans)

# BONUSSS

query = "SELECT COUNT(name) FROM titanic_table WHERE (Name LIKE 'Mr.%' OR Name LIKE 'Mrs.%') AND Siblings_Spouses_Aboard >= 1 "
ans = sl_curs.execute(query).fetchall()
ans

