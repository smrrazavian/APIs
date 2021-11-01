import sqlite3
from sqlite3 import Error

conn = sqlite3.connect(r'C:\Users\ASUS\Desktop\APIs\db\sample.db')
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS NUMBER")

sql ='''CREATE TABLE NUMBER(
    ID INT PRIMARY KEY,
    a INT NOT NULL,
    b INT NOT NULL,
    Result FLOAT
)'''

cursor.execute(sql)
print("Table created successfully........")
conn.commit()
