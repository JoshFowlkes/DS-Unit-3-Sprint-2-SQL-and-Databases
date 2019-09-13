import sqlite3 

# Make Connection 
conn = sqlite3.connect('northwind_small (1).sqlite3')
# Make Cursor 
curs = conn.cursor()

'''
curs.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY
name;").fetchall()
[('Category',), ('Customer',), ('CustomerCustomerDemo',),
('CustomerDemographic',), ('Employee',), ('EmployeeTerritory',), ('Order',),
('OrderDetail',), ('Product',), ('Region',), ('Shipper',), ('Supplier',),
('Territory',)]

curs.execute('SELECT sql FROM sqlite_master WHERE name="Customer";').fetchall()
[('CREATE TABLE "Customer" \n(\n  "Id" VARCHAR(8000) PRIMARY KEY, \n
"CompanyName" VARCHAR(8000) NULL, \n  "ContactName" VARCHAR(8000) NULL, \n
"ContactTitle" VARCHAR(8000) NULL, \n  "Address" VARCHAR(8000) NULL, \n  "City"
VARCHAR(8000) NULL, \n  "Region" VARCHAR(8000) NULL, \n  "PostalCode"
VARCHAR(8000) NULL, \n  "Country" VARCHAR(8000) NULL, \n  "Phone" VARCHAR(8000)
NULL, \n  "Fax" VARCHAR(8000) NULL \n)',)]
'''

# Queries
query = '''SELECT ProductName, UnitPrice
FROM Product
ORDER BY UnitPrice DESC
LIMIT 10'''
ans = curs.execute(query).fetchall()
print('Ten Most expensive items in descending order starting from highest:', ans)
print('\n')

query = '''
SELECT AVG(HireDate - BirthDate)
FROM Employee
'''
ans = curs.execute(query).fetchall()
print('Average age at the time of hire is: ', ans)
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
print('Ten Most expensive items in descending order starting from highest AND their supplier:', ans)
print('\n')


# largest category 
query = '''SELECT CategoryID, COUNT(CategoryId)
FROM Product
GROUP BY CategoryId
LIMIT 1'''
ans = curs.execute(query).fetchall()
print('LArgest Category by Distinct Products, Limit 1 :', ans)
print('\n')

# Stretch Goal
query = '''
SELECT FirstName, LastName, COUNT(EmployeeTerritory.EmployeeId)
FROM Employee JOIN EmployeeTerritory ON (Employee.Id = EmployeeTerritory.EmployeeId)
GROUP BY EmployeeTerritory.EmployeeId
ORDER BY COUNT(EmployeeTerritory.EmployeeId) DESC
'''
ans = curs.execute(query).fetchall()
print('\n')
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