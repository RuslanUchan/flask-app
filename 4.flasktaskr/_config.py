# Configuration file
import os

# folder where this script is located
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DATABASE = 'flasktaskr.db'
USERNAME = 'admin'
PASSWORD = 'admin'
WTF_CSRF_ENABLED = True  # config setting for XSS request prevention
SECRET_KEY = r'x83\xd4D\xb4\xc3\x865\xba\xc3\x8c\r;\xa3\x8b\xfc:\x94\xa8\xd5\x94\xee\xef='

# define the full path for the database
DATABASE_PATH = os.path.join(BASE_DIR, DATABASE)
