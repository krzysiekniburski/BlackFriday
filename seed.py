##
import pymysql as sql#
import random
from faker import Faker
fake = Faker()
conn = sql.Connect(host='localhost', unix_socket='', user='root', passwd='', db='agd')
cursor = conn.cursor()
for i in range(0, 10):
    a = fake.first_name()
    b = random.uniform(100, 8000)
    c = random.uniform(1, 100)


    ins = "INSERT INTO stuff (name, price, weight) VALUES (%s, %s, %s)"
    val = (a, b, c)
    cursor.execute(ins, val)
conn.commit()
