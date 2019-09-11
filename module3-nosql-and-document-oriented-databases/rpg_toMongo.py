pip install pymongo

import pymongo
import sqlite3

# Connecting to MongoDB, have to go to the webpage, create a new cluster, set up passw etc
client = pymongo.MongoClient("mongodb://<YOUR USER NAME HERE>:<YOUR PASSWORD>@cluster0-shard-00-00-t54y0.mongodb.net:27017,cluster0-shard-00-01-t54y0.mongodb.net:27017,cluster0-shard-00-02-t54y0.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client.test

# using sqlite3 to navigate the rpg data, be sure to add rpg database to this repository 
s1_conn = sqlite3.connect('rpg_db.sqlite3')
s1_curs = s1_conn.cursor()

# should return a value of 302, 
print(s1_curs.execute('SELECT COUNT(*) FROM charactercreator_character;').fetchall())

# Assinging a list of character for all characters from the database
characters = s1_curs.execute('SELECT * FROM charactercreator_character;').fetchall()

# to actually insert into MongoDB cluster that you have open
for i range(0,301):
    db.test.insert_one({
    'Character ID' : characters[i][0],
    'Name' : characters[i][1],
    'Level' : characters[i][2],
    'EXP' : characters[i][3],
    'HP' : characters[i][4],
    'Strength' : characters[i][5],
    'Intelligence' : characters[i][6],
    'Dexterity' : characters[i][7],
    'Wisdom' : characters[i][8]
    })

# Quick check into Mongo to see if worked, this will display all the entries currently in the MongoDB cluster
list(db.test.find())    