# Create SQLite3 table

import sqlite3

with sqlite3.connect("blog.db") as connection:
    c = connection.cursor()

    c.execute("CREATE TABLE posts(title TEXT, post TEXT)")

    # dummy data
    dummy = [
        ("Good", "I\'m good."),
        ("Well", "I\'m well"),
        ("Excellent", "I\'m excellent"),
        ("Okay", "I\'m okay")]

    c.executemany("INSERT INTO posts VALUES(?, ?)", dummy)
