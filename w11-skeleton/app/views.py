from flask import render_template, redirect, url_for, flash, request
from app import app, db
from app.forms import (LoginForm, RegistrationForm, ToDoForm, UploadForm)
from app.models import User, ToDo
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlsplit
from uuid import uuid4
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
import os
import csv
from email_validator import validate_email, EmailNotValidError


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        flash(f'Login for {form.username.data}', 'success')
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data,
                        password_hash=generate_password_hash(form.password.data, salt_length=32))
        db.session.add(new_user)
        try:
            db.session.commit()
            flash(f'Registration for {form.username.data} received', 'success')
            return redirect(url_for('index'))
        except:
            db.session.rollback()
            if User.query.filter_by(username=form.username.data):
                form.username.errors.append('This username is already taken. Please choose another')
            if User.query.filter_by(email=form.email.data):
                form.email.errors.append('This email address is already registered. Please choose another')
            flash(f'Registration failed', 'danger')
    return render_template('registration.html', title='Register', form=form)


def is_valid_email(email):
    try:
        validate_email(email, check_deliverability=False)
    except EmailNotValidError as error:
        return False
    return True


# Attempt to remove a file but silently cancel any exceptions if anything goes wrong
def silent_remove(filepath):
    try:
        os.remove(filepath)
    except:
        pass
    return


# Handler for 413 Error: "RequestEntityTooLarge". This error is caused by a file upload
# exceeding its permitted Capacity
# Note, you should add handlers for:
# 403 Forbidden
# 404 Not Found
# 500 Internal Server Error
# See: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
@app.errorhandler(413)
def error_413(error):
    return render_template('errors/413.html'), 413


@app.route('/todo', methods=['GET', 'POST'])
@login_required
def todo():
    form = ToDoForm()
    todo_list = ToDo.query.all()
    if form.validate_on_submit():
        db.session.commit()
        return redirect(url_for('todo'))
    return render_template('todo.html', title='ToDo', todo_list=todo_list, form=form)


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        if form.file.data:
            unique_str = str(uuid4())
            filename = secure_filename(f'{unique_str}-{form.file.data.filename}')
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            form.file.data.save(filepath)
            try:
                with open(filepath, newline='') as csvfile:
                    reader = csv.reader(csvfile)
                    error_count = 0
                    row = next(reader)

                    if row != ['Item', 'Priority']:
                        form.file.errors.append(
                            'First row of file must be a Header row containing "Item,Priority"')
                        raise ValueError()

                    for idx, row in enumerate(reader):
                        row_num = idx+2 # Spreadsheets have the first row as 0, and we skip the header
                        if error_count > 10:
                            form.file.errors.append('Too many errors found, any further errors omitted')
                            raise ValueError()
                        if len(row) != 2:
                            form.file.errors.append(f'Row {row_num} does not have precisely 4 fields')
                            error_count += 1
                        if ToDo.query.filter_by(username=row[0]).first():
                            form.file.errors.append(
                                f'Row {row_num} has username {row[0]}, which is already in use')
                            error_count += 1
                        if not is_valid_email(row[1]):
                            form.file.errors.append(f'Row {row_num} has an invalid email: "{row[1]}"')
                            error_count += 1
                        if ToDo.query.filter_by(email=row[1]).first():
                            form.file.errors.append(
                                f'Row {row_num} has email {row[1]}, which is already in use')
                            error_count += 1
                        if error_count == 0:
                            todo_list = ToDo(item=row[0], priority=row[1])
                            db.session.add(todo_list)

                if error_count > 0:
                   raise ValueError
                db.session.commit()
                flash(f'New todo Uploaded', 'success')

                return redirect(url_for('index'))
            except:
                flash(f'New todo upload failed: '
                      'please try again', 'danger')
                db.session.rollback()
            finally:
                silent_remove(filepath)
    return render_template('upload.html', title='Upload', form=form)
