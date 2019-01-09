from views import db
from models import Task
from datetime import date


# create the database and the table
db.create_all()

# insert data
# db.session.add(Task('Finish Real Python!', date(2018, 9, 3), 10, 1))
# db.session.add(Task('Finish Corey Flask!', date(2018, 9, 3), 10, 1))

# commit the changes
db.session.commit()
