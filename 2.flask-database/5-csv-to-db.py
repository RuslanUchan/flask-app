import csv
import sqlite3

with sqlite3.connect("new.db") as connection:
    c = connection.cursor()

    employees = csv.reader(open("employees.csv", "rU"))

    c.execute("CREATE TABLE employees(firstname TEXT, lastname TEXT)")

    # It will be useful to do try/except block
    try:
        c.executemany("INSERT INTO employees(firstname, lastname) \
                        VALUES(?,?)", employees)
    except sqlite3.OperationalError:
        print("Insertion into database failed")
