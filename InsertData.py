import pymysql as sql

conn = sql.Connect(host='localhost', unix_socket='', user='root', passwd='', db='agd')
cursor = conn.cursor()

stat = 'SELECT * FROM stuff'

cursor.execute(stat)

#cursor.fetchall()

lista = list(cursor.fetchall())

test_names = []
test_prices = []
test_weights = []

for row in lista:
    test_names.append(row[1])
    test_prices.append(row[2])
    test_weights.append(row[3])


print(test_names)
print(test_prices)
print(test_weights)

