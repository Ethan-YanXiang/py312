from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError
from app.models import Student, Loan
from sqlalchemy import and_


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirmpassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


class AddStudentForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    firstname = StringField('Firstname')
    lastname = StringField('Lastname', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Add Student')

    def validate_username(self, username):
        if Student.query.filter_by(username=username.data).first():
            raise ValidationError('This username is already taken. Please choose another')

    def validate_email(self, email):
        if Student.query.filter_by(email=email.data).first():
            raise ValidationError('This email address is already registered. Please choose another')


class BorrowForm(FlaskForm):
    student_id = StringField('Student ID', validators=[DataRequired()])
    device_id = StringField('Device ID', validators=[DataRequired()])
    submit = SubmitField('Borrow Device')

    def validate_student_id(self, student_id):
        if not student_id.data.isnumeric():
            raise ValidationError('This must be a positive integer')
        if not Student.query.get(student_id.data):
            raise ValidationError('There is no student with this id in the system')
        if Loan.query.filter(
                    (Loan.student_id == student_id.data)
                    &
                    # (Loan.returndatetime.is_(None))
                    (Loan.returndatetime.is_(None))
                ).first():
            raise ValidationError('This student cannot borrow another item until the previous loan has been returned')

    def validate_device_id(self, device_id):
        if not device_id.data.isnumeric():
            raise ValidationError('This must be a positive integer')
        if Loan.query.filter(
                    (Loan.device_id == device_id.data)
                    &
                    (Loan.returndatetime.is_(None))
                ).first():
            raise ValidationError('This device cannot be borrowed as it is currently on loan')
