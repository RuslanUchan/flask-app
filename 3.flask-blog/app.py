# Controller

from flask import Flask, render_template, request, session, \
    flash, redirect, url_for, g
import sqlite3
from functools import wraps

DATABASE = 'blog.db'
USERNAME = 'admin'
PASSWORD = 'admin'
# To get secret_key you can do
# import os
# os.urandom(24)
SECRET_KEY = "\x97\x97\xa4\xb86\xf7\x04\xb1/\x8cz\xc5\xf6\x8b&{\xdfKs\xdb\xfb\x14.p"

app = Flask(__name__)

# pulls in app configuration
app.config.from_object(__name__)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def login_required(test):
    """
    Check to see if logged_in is in the session
    if it is, then call appropriate function
    (the function that the decorator is applied to)
    if not, redirect user to the login page
    """
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to log in first.')
            return redirect(url_for('login'))
    return wrap


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    status_code = 200
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] or \
                request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid Credentials. Please try again.'
            status_code = 401
        else:
            session['logged_in'] = True
            return redirect(url_for('main'))
    return render_template('login.html', error=error), status_code


@app.route('/main')
@login_required
def main():
    """
    g are used as 'request blackboard' that gets wiped clean
    after request is finished
    it is best practice to use g when dealing with database connection
    """
    # Main homepage with Show Posts functionality
    g.db = connect_db()  # connect to the database
    c = g.db.execute('SELECT * FROM posts')  # cursor fetch data
    # create list of dictionaries of posts
    posts = [dict(title=row[0], post=row[1]) for row in c.fetchall()]
    g.db.close()
    return render_template('index.html', posts=posts)  # posts passed to html


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))


@app.route('/add', methods=['POST'])
@login_required
def add():
    title = request.form['title']
    post = request.form['post']
    if not title or not post:
        flash('All fields are required. Please try again')
        return redirect(url_for('main'))
    else:
        g.db = connect_db()
        g.db.execute('Insert into posts (title, post) values (?, ?)',
                     [request.form['title'], request.form['post']])
        g.db.commit()
        g.db.close()
        flash('New entry was posted!')
        return redirect(url_for('main'))


if __name__ == "__main__":
    app.run(debug=True)
