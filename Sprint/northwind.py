import sqlite3 

# Make Connection 
conn = sqlite3.connect('northwind_small.sqlite3')
# Make Cursor 
curs = conn.cursor()

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

# Queries
query = '''SELECT ProductName, UnitPrice
FROM Product
ORDER BY UnitPrice DESC
LIMIT 10'''
ans = curs.execute(query)
print('Ten Most expensive items in descending order starting from highest:', ans)

query = '''
SELECT AVG(HireDate - BirthDate)
FROM Employee
'''
ans = curs.execute(query)
print('Average age at the time of hire is: ', ans)

# Stretch Question
query = '''
SELECT City, AVG(HireDate - BirthDate)
FROM Employee
GROUP BY City
'''
ans = curs.execute(query)
print('Average age at the time of hire Grouped by City is: ', ans)

# now for the joins Queries
query = '''SELECT ProductName, UnitPrice, Supplier.CompanyName
FROM Product  JOIN Supplier ON (Product.SupplierId=Supplier.Id)
ORDER BY UnitPrice DESC
LIMIT 10'''
ans = curs.execute(query)
print('Ten Most expensive items in descending order starting from highest AND their supplier:', ans)


# largest category 
query = '''SELECT CategoryID, COUNT(CategoryId)
FROM Product
GROUP BY CategoryId
LIMIT 1'''
ans = curs.execute(query)
print('LArgest Category by Distinct Products, Limit 1 :', ans)