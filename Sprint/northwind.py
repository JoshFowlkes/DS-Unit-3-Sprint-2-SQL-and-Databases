import sqlite3 

# Make Connection 
conn = sqlite3.connect('northwind_small (1).sqlite3')
# Make Cursor 
curs = conn.cursor()


# Queries
# ten most expensive products 
query = '''SELECT ProductName, UnitPrice
FROM Product
ORDER BY UnitPrice DESC
LIMIT 10'''
ans = curs.execute(query).fetchall()
print('\n')
print('Ten Most expensive items in descending order starting from highest:', ans)
print('\n')


# avg age at hire date
query = '''
SELECT AVG(HireDate - BirthDate)
FROM Employee
'''
ans = curs.execute(query).fetchall()
print('Average age at the time of hire is: ', ans[0][0])
print('\n')


# Stretch Question
query = '''
SELECT City, AVG(HireDate - BirthDate)
FROM Employee
GROUP BY City
'''
ans = curs.execute(query).fetchall()
print('Average age at the time of hire Grouped by City is: ', ans)
print('\n')


# now for the joins Queries
query = '''SELECT ProductName, UnitPrice, Supplier.CompanyName
FROM Product  JOIN Supplier ON (Product.SupplierId=Supplier.Id)
ORDER BY UnitPrice DESC
LIMIT 10'''
ans = curs.execute(query).fetchall()
print('Ten Most expensive items, The Price, The Supplier. All in descending order: ', ans)
print('\n')


# largest category 
query = '''SELECT CategoryID, COUNT(CategoryId)
FROM Product
GROUP BY CategoryId
LIMIT 1'''
ans = curs.execute(query).fetchall()
print('LArgest Category by Distinct Products, Limit 1, and the number of products :', ans)
print('\n')


# Stretch Goal
query = '''
SELECT FirstName, LastName, COUNT(EmployeeTerritory.EmployeeId)
FROM Employee JOIN EmployeeTerritory ON (Employee.Id = EmployeeTerritory.EmployeeId)
GROUP BY EmployeeTerritory.EmployeeId
ORDER BY COUNT(EmployeeTerritory.EmployeeId) DESC
LIMIT 1;
'''
ans = curs.execute(query).fetchall()
print('The Employee with the most Territories is and the count :', ans)
print('\n')




'''
------OPEN ENDED QUESTIONS -------
Question 1:
The 'Employee' and 'Territory' Tables Are relational in nature. In the territory table there is a column named 'EmployeeID'.
This relates back to the 'Employee' table in that that for each indivual 'EmployeeId' in the 'Territory' table, there is detailed
information about that employee in the 'Employee' table. 

Question 2:
You would use something like MongoDB when you need something that is high in availability and high in ability to scale. 
Some examples would be a product catalog and storing the data for blogs.
It would be BAD to use it in a transactional situation, say storing data at a bank. Ie someone could make a withdrawel, 
then another withdrawel even if they didn't actually have the money for it but the database simply didn't have the latest data
available yet. 

Question 3:
NewSQL attempts to solve the problems that SQL and NoSql could not solve on their own. Primarily in keeping true to the ACID principles, 
and scalability. Take for example the answer in question2, NewSQL attempts to solve the problem by being both highly scalable, AND able to 
have the latest data readily available as quickly as possible to avoid the issue that happens in the bank account withdrawel example. 

'''



'''
--------- THE OUT PUTS FOR FACILITATED GRADING -----------
Ten Most expensive items in descending order starting from highest: [('Côte de Blaye', 263.5), ('Thüringer Rostbratwurst', 123.79), ('Mishi Kobe Niku', 97), ("Sir Rodney's Marmalade", 81), ('Carnarvon Tigers', 62.5), ('Raclette Courdavault', 55), ('Manjimup Dried Apples', 53), ('Tarte au sucre', 49.3), ('Ipoh Coffee', 46), ('Rössle Sauerkraut', 45.6)]


Average age at the time of hire is:  37.22222222222222


Average age at the time of hire Grouped by City is:  [('Kirkland', 29.0), ('London', 32.5), ('Redmond', 56.0), ('Seattle', 40.0), ('Tacoma', 40.0)]


Ten Most expensive items, The Price, The Supplier. All in descending order:  [('Côte de Blaye', 263.5, 'Aux joyeux ecclésiastiques'), ('Thüringer Rostbratwurst', 123.79, 'Plutzer Lebensmittelgroßmärkte AG'), ('Mishi Kobe Niku', 97, 'Tokyo Traders'), ("Sir Rodney's Marmalade", 81, 'Specialty Biscuits, Ltd.'), ('Carnarvon Tigers', 62.5, 'Pavlova, Ltd.'), ('Raclette Courdavault', 55, 'Gai pâturage'), ('Manjimup Dried Apples', 53, "G'day, Mate"), ('Tarte au sucre', 49.3, "Forêts d'érables"), ('Ipoh Coffee', 46, 'Leka Trading'), ('Rössle Sauerkraut', 45.6, 'Plutzer Lebensmittelgroßmärkte AG')]


Largest Category by Distinct Products, Limit 1, and the number of products : [(1, 12)]


The Employee with the most Territories is and the count : [('Robert', 'King', 10)]

'''
