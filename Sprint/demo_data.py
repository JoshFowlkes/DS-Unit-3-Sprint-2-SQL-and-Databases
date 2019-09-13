import sqlite3

# Make Connection 
conn = sqlite3.connect('demo_data.sqlite3')
# Make Cursor 
curs = conn.cursor()

create_table = """
CREATE TABLE demo (
    s TEXT,
    x INT,
    y INT
);
"""
curs.execute(create_table)

insert_data = """
INSERT INTO demo 
(s, x, y)
VALUES ('g', 3, 9),
       ('v', 5, 7),
       ('f', 8, 7)  
"""
curs.execute(insert_data)
conn.commit()

query = 'SELECT COUNT(s) FROM demo'
ans = curs.execute(query).fetchall()
print('Number of Rows: ', ans)

query = 'SELECT COUNT(s) FROM demo WHERE x >= 5 AND y >= 5'
ans = curs.execute(query).fetchall()
print('Number of rows where x and y are at least 5: ', ans)

query = 'SELECT COUNT(DISTINCT y) FROM demo'
ans = curs.execute(query).fetchall()
print('Number of unqiue Y values: ', ans)

