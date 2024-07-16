from flask import render_template, redirect, url_for, flash
from app import app, db
from datetime import datetime
from app.forms import LoginForm, RegistrationForm, AddStudentForm, BorrowForm, DeactivateStudentForm, ReturnLoanForm
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
    if form.validate_on_submit():
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
    if form.validate_on_submit():
        new_student = Student(username=form.username.data, firstname=form.firstname.data,
                              lastname=form.lastname.data, email=form.email.data)
        db.session.add(new_student)
        try:
            db.session.commit()
            flash(f'New Student added: {form.username.data} received', 'success')
            return redirect(url_for('index'))
        except:
            db.session.rollback()
            if Student.query.filter_by(username=form.username.data).first():
                form.username.errors.append('This username is already taken. Please choose another')
            if Student.query.filter_by(email=form.email.data).first():
                form.email.errors.append('This email address is already registered. Please choose another')
    return render_template('add_student.html', title='Add Student', form=form)


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


# 1a
@app.route('/listStudents', methods=['GET', 'POST'])
def listStudents():
    students = Student.query.all()
    return render_template('listStudents.html', title='List Students', students=students)


# 1a
@app.route('/deactivate', methods=['GET', 'POST'])
def deactivateStudent():
    form = DeactivateStudentForm()
    if form.validate_on_submit():
        student = Student.query.get(form.student_id.data)
        student.active = False
        db.session.add(student)
        try:
            db.session.commit()
            flash(f'student {student} deactivated', 'success')
            return redirect(url_for('index'))
        except:
            db.session.rollback()
    return render_template('deactivateStudent.html', title='Deactivate Student', form=form)


# 1b
@app.route('/listLoans', methods=['GET', 'POST'])
def listLoans():
    loans = Loan.query.all()
    return render_template('listLoans.html', title='List Loans', loans=loans)


@app.route('/return', methods=['GET', 'POST'])
def returnLoan():
    form = ReturnLoanForm()
    if form.validate_on_submit():
        loan = Loan.query.filter(
            (Loan.student_id == form.student_id.data)
            &
            (Loan.device_id == form.device_id.data)
            &
            (Loan.returndatetime.is_(None))
        ).first()
        loan.returndatetime = datetime.now()
        loan.damaged = form.damaged.data
        db.session.add(loan)
        try:
            db.session.commit()
            flash(f'Loan return processed: {loan}', 'success')
            return redirect(url_for('index'))
        except:
            db.session.rollback()
    return render_template('return.html', title='Return', form=form)
