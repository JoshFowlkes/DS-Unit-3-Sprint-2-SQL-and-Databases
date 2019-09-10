import sqlite3

"""Printing all the column names"""
#curs.execute("SELECT name FROM sqlite_master WHERE type='table';")
#print(curs.fetchall())

def conx_sqlite(db):
    cnx = sqlite3.connect(db)
    return cnx

def run_queries(c):
    query = ''' SELECT COUNT(character_id) FROM charactercreator_character '''
    for row in c.execute(query):
        print('Question 1: Count of all Characters: ', row[0])

    """ Characters in Each Subclass """
    query = '''
    SELECT COUNT(character_ptr_id) FROM charactercreator_cleric
    ''' 
    for row in c.execute(query):
        print(row[0], 'Clerics')

    query = '''
    SELECT COUNT(character_ptr_id) FROM charactercreator_fighter
    ''' 
    for row in c.execute(query):
        print(row[0], 'Fighters')

    query = '''
    SELECT COUNT(character_ptr_id) FROM charactercreator_thief
    '''
    for row in c.execute(query):
        print(row[0], 'Thieves')

    query = '''
    SELECT COUNT(character_ptr_id) FROM charactercreator_mage
    '''             
    for mage in c.execute(query):
        query2 = 'SELECT COUNT(mage_ptr_id) FROM charactercreator_necromancer'
        for necro in c.execute(query2):
            print('There are', mage[0], 'Mages, and out of that, there are', necro[0], 'Necromancers.')

    print()

    """ Items Count """           
    for i in c.execute('SELECT COUNT(item_id) FROM armory_item'):
        print('There are', i[0], 'Total Items.')
    """ Weapons Count """
    for w in c.execute('SELECT COUNT(item_ptr_id) FROM armory_weapon'):
        print(w[0], 'Weapons')
    print((i[0] - w[0]), 'Items that are not Weapons')
    print()
    

    """ How many items does each character have? """
    query1 = '''
    SELECT character.name, count(item.item_id) as item_count
          FROM charactercreator_character AS character,
        JOIN charactercreator_character_inventory AS inventory
          ON character.character_id = inventory.character_id
        JOIN armory_item AS item
          ON inventory.item_id = item.item_id
        GROUP BY character.name
        LIMIT 5
    '''
    print('Character | Item')
    rows = c.execute(query1)
    for row in rows:
        name = row[0]
        print(name, ' | ' ,row[1])






def main():
    con = conx_sqlite('rpg_db.sqlite3')
    curs = con.cursor()
    run_queries(curs)
    curs.close()
    con.close()   # Close the connection
    return

if __name__ == '__main__':
    print('\n'*20)  # force teminal to clear screen
    main()