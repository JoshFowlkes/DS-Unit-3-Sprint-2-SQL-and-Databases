import sqlite3

# Make Connection and Cursor
conn = sqlite3.connect('demo_data.sqlite3')
curs = conn.cursor()


create_table = """
CREATE TABLE demo (
    s TEXT,
    x INT,
    y INT
);
"""
# the next line is commented out so as not to create a new table
#curs.execute(create_table)


insert_data = """
INSERT INTO demo 
(s, x, y)
VALUES ('g', 3, 9),
       ('v', 5, 7),
       ('f', 8, 7)  
"""
# the next line is commented out so as not to reinsert new data into the table
#curs.execute(insert_data)
#conn.commit()


# Number of Rows
query = 'SELECT COUNT(s) FROM demo'
ans = curs.execute(query).fetchall()
print('Number of Rows: ', ans[0][0])


# Number of Rows Where both X and Y are greater/equal to 5
query = 'SELECT COUNT(s) FROM demo WHERE x >= 5 AND y >= 5'
ans = curs.execute(query).fetchall()
print('Number of rows where x and y are at least 5: ', ans[0][0])


# Number of Distinct Y Values
query = 'SELECT COUNT(DISTINCT y) FROM demo'
ans = curs.execute(query).fetchall()
print('Number of unqiue Y values: ', ans[0][0])

