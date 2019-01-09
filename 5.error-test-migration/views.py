from forms import AddTaskForm, RegisterForm, LoginForm
from functools import wraps
from flask import (Flask, flash, redirect, render_template, request, session,
                   url_for)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import datetime

# config
app = Flask(__name__)
app.config.from_object('_config')
db = SQLAlchemy(app)

# Avoiding circular imports
from models import Task, User


# helper function
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first!')
            return redirect(url_for('login'))
    return wrap


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u'Error in the %s field - $s' % (
                getattr(form, field).label.text, error), 'error')


def open_tasks():
    return db.session.query(Task).filter_by(
        status='1').order_by(Task.due_date.asc())


def closed_tasks():
    return db.session.query(Task).filter_by(
        status='0').order_by(Task.due_date.asc())


# route handlers
@app.route('/logout/')
@login_required
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    session.pop('role', None)
    flash('Goodbye!')
    return redirect(url_for('login'))


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(name=request.form['name']).first()
            if user is not None and user.password == request.form['password']:
                session['logged_in'] = True
                session['user_id'] = user.id  # log user_id in the session
                session['role'] = user.role
                flash('Welcome!')
                return redirect(url_for('tasks'))
            else:
                error = 'Invalid username or password.'
    return render_template('login.html', form=form, error=error)


@app.route('/tasks/')
@login_required
def tasks():
    """
    Get query of open tasks and closed tasks from the database,
    Render it on the tasks.html
    """
    open_tasks = db.session.query(Task) \
        .filter_by(status='1').order_by(Task.due_date.asc())
    closed_tasks = db.session.query(Task) \
        .filter_by(status='0').order_by(Task.due_date.asc())
    return render_template(
        'tasks.html',
        form=AddTaskForm(request.form),
        open_tasks=open_tasks(),
        closed_tasks=closed_tasks()
    )


# Add new tasks
@app.route('/add/', methods=['GET', 'POST'])
@login_required
def new_task():
    error = None
    form = AddTaskForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_task = Task(
                form.name.data,
                form.due_date.data,
                form.priority.data,
                '1',
                datetime.datetime.utcnow(),
                session['user_id']  # add user session into the database
            )
            # Add the data in the session when creating new instance
            # When updating or delete, no need to do session.add
            db.session.add(new_task)
            db.session.commit()
            flash('New entry created!')
            return redirect(url_for('tasks'))
    # If the request is GET
    return render_template(
        'tasks.html',
        form=form,
        error=error,
        open_tasks=open_tasks(),
        closed_tasks=closed_tasks()
    )


# Mark tasks as complete
@app.route('/complete/<int:task_id>/')
@login_required
def complete(task_id):
    new_id = task_id
    task = db.session.query(Task).filter_by(task_id=new_id)
    if session['user_id'] == task.first().used_id or session['role'] == "admin":
        # Check if the user completed is the actual user
        task.update({'status': '0'})
        db.session.commit()
        flash('Task marked complete!')
        return redirect(url_for('tasks'))
    else:
        flash('You can only update tasks that belong to you')
        return redirect(url_for('tasks'))


# Delete tasks
@app.route('/delete/<int:task_id>/')
@login_required
def delete_entry(task_id):
    new_id = task_id
    task = db.session.query(Task).filter_by(task_id=new_id)
    if session['user_id'] == task.first().used_id or session['role'] == "admin":
        task.delete()
        db.session.commit()
        flash('Task deleted!')
        return redirect(url_for('tasks'))
    else:
        flash('You can only delete tasks that belong to you')
        return redirect(url_for('tasks'))


# Register route
@app.route('/register/', methods=['GET', 'POST'])
def register():
    error = None
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_user = User(
                form.name.data,
                form.email.data,
                form.password.data
            )
            try:
                db.session.add(new_user)
                db.session.commit()
                flash('Registration Success! Please login.')
                return redirect(url_for('login'))
            except IntegrityError:
                error = 'Username and/or email already taken!'
                return render_template('register.html', form=form, error=error)
    return render_template('register.html', form=form, error=error)
