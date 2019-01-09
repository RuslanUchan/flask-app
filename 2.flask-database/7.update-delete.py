import sqlite3

with sqlite3.connect("new.db") as connection:
    c = connection.cursor()

    # Do update
    c.execute("UPDATE population\
                SET population = 9000000 WHERE city = 'New York City'")

    # Do delete
    c.execute("DELETE FROM population WHERE city='Boston'")

    print("\nNEW DATA:\n")
    c.execute("SELECT * FROM population")
    rows = c.fetchall()

    for row in rows:
        print(row[0], row[1], row[2])
