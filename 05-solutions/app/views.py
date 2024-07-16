from flask import render_template, redirect, url_for, flash
from app import app, db
from datetime import datetime
from app.forms import LoginForm, RegistrationForm, AddStudentForm, RemvStudentForm, BorrowForm, ReturnForm, ReportForm
from app.models import Student, Loan


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/datetime')
def date_time():
    now = datetime.now()
    return render_template('datetime.html', title='Date & Time', now=now)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():  # call the validators
        flash(f'Login for {form.username.data}', 'success')
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Registration for {form.username.data} received', 'success')
        return redirect(url_for('index'))
    return render_template('registration.html', title='Register', form=form)


@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    form = AddStudentForm()
    if form.validate_on_submit():  # store collected data to Student table
        new_student = Student(username=form.username.data, firstname=form.firstname.data,
                              lastname=form.lastname.data, email=form.email.data)
        db.session.add(new_student)
        try:
            db.session.commit()
            flash(f'New Student added: {form.username.data} received', 'success')
            return redirect(url_for('index'))
        except:
            db.session.rollback()  # we want to append the errors if somehow fail to commit although pass all the validators
            if Student.query.filter_by(username=form.username.data).first():  # giving user the reason which one is fail, and set the error message
                form.username.errors.append('This username is already taken. Please choose another')
            if Student.query.filter_by(email=form.email.data).first():
                form.email.errors.append('This email address is already registered. Please choose another')
    return render_template('add_student.html', title='Add Student', form=form)


@app.route('/remove_student', methods=['GET', 'POST'])
def remove_student():
    form = RemvStudentForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(username=form.username.data).first()
        if student:
            loans = Loan.query.filter_by(student_id=student.student_id).all()
            for loan in loans:
                if loan.returndatetime is None:
                    flash('Cannot remove student, student has loans', 'danger')
                else:
                    db.session.delete(student)
                    try:
                        db.session.commit()
                        flash('Student removed successfully', 'success')
                        return redirect(url_for('index'))
                    except:
                        db.session.rollback()
    return render_template('remove.html', title='Remove Student', form=form)


@app.route('/borrow', methods=['GET', 'POST'])
def borrow():
    form = BorrowForm()
    if form.validate_on_submit():
        new_loan = Loan(device_id=form.device_id.data,
                        student_id=form.student_id.data,
                        borrowdatetime=datetime.now())

        db.session.add(new_loan)
        try:
            db.session.commit()
            flash(f'New Loan added', 'success')
            return redirect(url_for('index'))
        except:
            db.session.rollback()
    return render_template('borrow.html', title='Borrow', form=form)


@app.route('/return', methods=['GET', 'POST'])
def return_device():
    form = ReturnForm()
    if form.validate_on_submit():
        loan = Loan.query.filter_by(device_id=form.device_id.data, returndatetime=None).first()
        if loan:
            loan.returndatetime = datetime.now()
            try:
                db.session.commit()
                flash('Loan updated successfully', 'success')
                return redirect(url_for('index'))
            except:
                db.session.rollback()
                flash('Failed to update loan', 'danger')

    return render_template('return.html', title='Return', form=form)


@app.route('/report', methods=['GET', 'POST'])
def display_report():
    form = ReportForm()
    if form.validate_on_submit():
        if form.report_type.data == 'student':
            student = Student.query.filter_by(student_id=form.input_id.data).first()
            if student:
                loans = Loan.query.filter_by(student_id=student.student_id).all()
                return render_template('student_report.html', student=student, loans=loans)
            else:
                flash('Student not found', 'danger')

        elif form.report_type.data == 'device':
            loans = Loan.query.filter_by(device_id=form.input_id.data).all()
            return render_template('device_report.html', loans=loans, device_id=form.input_id.data)
    return render_template('report.html', title='Generate Report', form=form)
