from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, BooleanField  # 1b
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

# 1a
        student = Student.query.get(student_id.data)
        if not (student):
            raise ValidationError('There is no student with this id in the system')
        if not student.active:
            raise ValidationError('This student has been deactivated and cannot borrow devices')

        if Loan.query.filter(
                    (Loan.student_id == student_id.data)
                    &
                    (Loan.returndatetime.is_(None))
                ).first():
            raise ValidationError('This student cannot borrow another item until the previous loan has been returned')
# 1b
        if Loan.query.filter(
                    (Loan.student_id == student_id.data)
                    &
                    (Loan.damaged is True)
                ).first():
            raise ValidationError('This student cannot borrow they haven\'t yet compensated for previous damaged return')

    def validate_device_id(self, device_id):
        if not device_id.data.isnumeric():
            raise ValidationError('This must be a positive integer')
        if Loan.query.filter(
                    (Loan.device_id == device_id.data)
                    &
                    (Loan.returndatetime.is_(None))
                ).first():
            raise ValidationError('This device cannot be borrowed as it is currently on loan')


# 1a
class DeactivateStudentForm(FlaskForm):
    student_id = StringField('Student ID', validators=[DataRequired()])
    submit = SubmitField('Deactivate Student')

    def validate_student_id(self, student_id):
        if not student_id.data.isnumeric():
            raise ValidationError('This must be a positive integer')
        student = Student.query.get(student_id.data)
        if not student:
            raise ValidationError('There is no student with this id in the system')
        if not student.active:
            raise ValidationError('This student has already been deactivated')


# 1b
class ReturnLoanForm(FlaskForm):
    student_id = StringField('Student ID', validators=[DataRequired()])
    device_id = StringField('Device ID', validators=[DataRequired()])
    damaged = BooleanField('Damaged', default=False)
    submit = SubmitField('Return Device')

    def validate_student_id(self, student_id):
        if not student_id.data.isnumeric():
            raise ValidationError('This must be a positive integer')
        if not Student.query.get(student_id.data):
            raise ValidationError('There is no student with this id in the system')
# 1b
        if not Loan.query.filter(
                (Loan.student_id == student_id.data)
                &
                (Loan.device_id == self.device_id.data)
                &
                (Loan.returndatetime.is_(None))
        ).first():
            raise ValidationError('This student does not currently have this device on loan')

    def validate_device_id(self, device_id):
        if not device_id.data.isnumeric():
            raise ValidationError('This must be a positive integer')
# 1b
        if not Loan.query.filter(
                (Loan.student_id == self.student_id.data)
                &
                (Loan.device_id == device_id.data)
                &
                (Loan.returndatetime.is_(None))
        ).first():
            raise ValidationError('This device cannot be returned as it has been returned')
