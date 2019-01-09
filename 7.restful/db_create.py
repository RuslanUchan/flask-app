# from datetime import date

from project import db
# from project.models import Task, User


# create the database and the table
db.create_all()

# insert data
# db.session.add(User('admin', 'ad@min.com', 'admin', 'admin'))
# db.session.add(Task(
#     'Finish Real Python!', date(2018, 9, 3), 10, 1, date(2018, 9, 26), 1))
# db.session.add(Task(
#     'Finish Corey Flask!', date(2018, 9, 3), 10, 1, date(2018, 9, 26), 1))

# commit the changes
db.session.commit()
