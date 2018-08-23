import sqlite3

connection = sqlite3.connect("new.db")

cursor = connection.cursor()

cursor.execute("INSERT INTO population \
                VALUES('New York City', 'NY', 8400000)")
cursor.execute("INSERT INTO population \
               VALUES('San Fransisco', 'CA', 800000)")

connection.commit()
connection.close()
