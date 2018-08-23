# Create a SQLite3 database and table

# Import libraries
import sqlite3

# create a new database if doesn't already exist
connection = sqlite3.connect("new.db")

# get a cursor object used to execute SQL commands
c = connection.cursor()

# create a table
c.execute("""CREATE TABLE population
                (city TEXT, state TEXT, population INT)
                """)

# close the connection
connection.close()
