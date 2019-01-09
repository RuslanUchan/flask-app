import os
import sys
import tempfile

# Add module to syspath
# Get current working directory
cwd = os.path.abspath(os.path.dirname(__file__))
print(cwd)

# isolate our current folder
project = os.path.basename(cwd)
print(project)

# remove the last folder from cwd
new_path = cwd.strip(project)
print(new_path)

# create new path to Flask object
# full_path = os.path.join(new_path, 'flaskr')
# print(full_path)

try:
    from flaskr import app, init_db
except ImportError:
    sys.path.append(new_path)
    from flaskr import app, init_db

"""
Set up a test database by creating a completely new database via
tempfile.mkstemp() and remove it after feature testing is done
"""


def before_feature(context, feature):
    # test the mock-up application
    app.config['TESTING'] = True
    context.db, app.config['DATABASE'] = tempfile.mkstemp()
    context.client = app.test_client()
    init_db()


def after_feature(context, feature):
    os.close(context.db)
    os.unlink(app.config['DATABASE'])
