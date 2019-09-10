#!pip install psycopg2-binary
# alternatively you can use in command line:
# conda install -c anaconda psycopg2
import psycopg2
import sqlite3
dir(psycopg2.connect)
help(psycopg2.connect)

# dont commit  password, 
dbname = ''
user = ''
password = '' # DONT COMMIT THIS
host = ''

pg_conn = psycopg2.connect(dbname = dbname, user = user,
                        password = password, host = host)

# assigning cursor
pg_curs = pg_conn.cursor()

# doing a quick search like did in lecture and in training kit
# this should fetch JSON file without having to install it, psycopg will handle it
pg_curs.execute('SELECT * FROM test_table;')
pg_curs.fetchall()

"""
What we're doing: 
We'd like to get the RPG data out of SQLite and inset it into PostgreSQL
AKA - we're making a data pipeline! AKA ETL(Extract, Transform, Load)
"""

# using wget to get the raw rpg SQL database
# try urlib here also and see if it works 
import urllib.request
import wget
url = 'https://github.com/JoshFowlkes/DS-Unit-3-Sprint-2-SQL-and-Databases/blob/master/module1-introduction-to-sql/rpg_db.sqlite3'
wget.download(url, '/Users/Inceptive/Desktop/githubrepos/DS-Unit-3-Sprint-2-SQL-and-Databases/module2-sql-for-analysis')

# renaming the ugly file name
#mv('rpg_db.sqlite3?raw=true', rpg_db.sqlite3)

# bringing in via sqlite3
import sqlite3
s1_conn = sqlite3.connect('rpg_db.sqlite3')
s1_curs = s1_conn.cursor()

# quick query check to see that it worked,
# a query of selecting the count of all names, from database 'charactercreator_character, then fetchall() displays
s1_curs.execute('SELECT COUNT(name) FROM charactercreator_character;').fetchall()

# bringing in the table characters specifically
characters = s1_curs.execute('SELECT * FROM charactercreator_character;').fetchall()

# quick check to display first character
characters[0]

# quick check on last character
characters[-1]

# this should be 302 
len(characters)

# EXTRACT done! Next step Transform
# We need the PostgreSQL db to have a table with an appropriate schema
create_character_table = """
    CREATE TABLE charactercreator_character (
        character_id SERIAL PRIMARY KEY,
        name VARCHAR(30),
        level INT,
        exp INT,
        hp INT,
        strength INT,
        intelligence INT,
        dexterity INT,
        wisdom INT
    );
"""
# This execute makes the table, thats why no fetchall() here
pg_curs.execute(create_character_table)

# WE can query tables if we want to check
# this is a clever optional thing, showing postgreSQL internals
show_tables = """ 
SELECT
    *
FROM
    pg_catalog.pg_tables
WHERE
    schemaname != 'pg_catalog'
AND schemaname != 'information_schema';
 """
pg_curs.execute(show_tables)
pg_curs.fetchall()

# Transofmr(making the target ready to get data) done, Now we need to actually load values
# Now we need to insert actual character
str(characters[0][1:]) # this is what we want to insert

example_insert = """
INSERT INTO charactercreator_character
(name, level, exp, hp, strength, intelligence, dexterity, wisdom)
VALUES """ + str(characters[0][1:])

print(example_insert)

# this is a single character, how do we do this for all the characters?
# LOOPS!
for character in characters:
    insert_character = """
    INSERT INTO charactercreator_character
    (name, level, exp, hp, strength, intelligence, dexterity, wisdom)
    VALUES """ + str(character[1:]) + ';'
    print(insert_character) # check out what this is doing
    pg_curs.execute(insert_character) # this actually adds them  the database on here, (NOt sql, have to commit )

# now these should appear in the elephant sql playground I made
# NOW, simply repeat these steps with Titanic Data    

# this will check within the py file
pg_curs.execute('SELECT * FROM charactercreator_character;')
pg_curs.fetchall()

# TO actually Commit to elephantSQL
pg_curs.close() # this closes the cursor
pg_conn.commit() # this.... you guessed it, commits

""" From here, go check elephantSQL and it should be on there """

# Now to check programmatically
pg_curs = pg_conn.cursor()
pg_curs.execute('SELECT * FROM charactercreator_character;')
pg_characters = pg_curs.fetchall() # we call it pg_characters because we already have characters above, and now can compare

assert(characters[0] == pg_characters) # this should check out to be true here, and print out same results

# now to loop over and check them all, this is how you zip
for character, pg_characters in zip(character, pg_characters):
    assert character == pg_characters


""" And with that, I've successfully done my first ETL """    