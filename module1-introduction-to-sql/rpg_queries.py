import sqlite3

conn = sqlite3.connect('rpg_db.sqlite3')
curs = conn.cursor()
print('-------- RPG QUESTIONS -------')
"""Question 1: Count of all characters """
query = '''SELECT COUNT(character_id) FROM charactercreator_character'''
results = curs.execute(query)
print('Total Number of Characters:', results.fetchall()[0][0])

"""Question 2: How many of each specific subclass? """
query = '''SELECT COUNT(character_ptr_id) FROM charactercreator_cleric'''
results = curs.execute(query)
print('Total Number of Clerics', results.fetchall()[0][0])

query = '''SELECT COUNT(character_ptr_id) FROM charactercreator_fighter'''
results = curs.execute(query)
print('Total Number of Fighters', results.fetchall()[0][0])

query = '''SELECT COUNT(character_ptr_id) FROM charactercreator_mage'''
results = curs.execute(query)
print('Total Number of Mages', results.fetchall()[0][0])

query = '''SELECT COUNT(mage_ptr_id) FROM charactercreator_necromancer'''
results = curs.execute(query)
print('Total Number of Necromancers', results.fetchall()[0][0])

query = '''SELECT COUNT(character_ptr_id) FROM charactercreator_thief'''
results = curs.execute(query)
print('Total Number of Thieves', results.fetchall()[0][0])

"""Question 3: How many total Items?"""
query = '''SELECT COUNT(item_id) FROM armory_item'''
results = curs.execute(query)
print('Total Number of Items: ', results.fetchall()[0][0])

"""Question 4: How many of the Items are weapons? How many are not?"""
query = """SELECT COUNT(ai.item_id)
FROM armory_item as ai, armory_weapon as aw
WHERE ai.item_id = aw.item_ptr_id"""
results = curs.execute(query)
print("Weapons: ", results.fetchall()[0][0])


"""Question 5: How many Items does each character have? (Return first 20 rows)"""
query = ''' SELECT character_id, item_id, COUNT(*)
FROM charactercreator_character_inventory
GROUP BY character_id 
LIMIT 20;'''
results = curs.execute(query)
matrix = results.fetchall()
item_list = []
for row in matrix:
    item_list.append(row[2])
print('Number of items for first 20 characters: ', item_list)  

"""Question 6: How many Weapons does each character have? (Return first 20 rows)"""
query = """SELECT character_id, item_id, COUNT(*)
FROM charactercreator_character_inventory
WHERE item_id IN (SELECT item_ptr_id FROM armory_weapon)
GROUP BY character_id
LIMIT 20;
"""
results = curs.execute(query)
matrix = results.fetchall()
weapon_list = []
for row in matrix:
    weapon_list.append(row[2])
    
"""Question 7: On average, how many Items does each Character have?"""
query = """SELECT AVG(counted) FROM (
SELECT character_id, item_id, COUNT(*) AS counted
FROM charactercreator_character_inventory
GROUP BY character_id);
"""
results = curs.execute(query)
print("Avg. Items per Character: ", results.fetchall()[0][0])

"""Question 8: On average, how many Weapons does each character have?"""
query = """SELECT AVG(counted) FROM (
SELECT character_id, item_id, COUNT(*) AS counted
FROM charactercreator_character_inventory
WHERE item_id IN (SELECT item_ptr_id FROM armory_weapon)
GROUP BY character_id);
"""
results = curs.execute(query)
print("Avg. Weapons per Character: ", results.fetchall()[0][0])