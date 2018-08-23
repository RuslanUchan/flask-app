import sqlite3
from _config import DATABASE_PATH

with sqlite3.connect(DATABASE_PATH) as connection:
    # get a cursor object
    c = connection.cursor()

    # create the table
    c.execute("""CREATE TABLE tasks(task_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        due_date TEXT NOT NULL,
        priority INTEGER NOT NULL,
        status INTEGER NOT NULL)""")

    # insert dummy data
    tasks = [
        ('Finish the tutorial!', '9/3/2018', 10, 1),
        ('Finish Real Python course 2', '9/3/2018', 10, 1)]

    # auto increment ids === not having to put them explicitly
    c.executemany('INSERT INTO tasks(name, due_date, priority, status)'
                  'VALUES(?, ?, ?, ?)', tasks)
