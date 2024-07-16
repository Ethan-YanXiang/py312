from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.fields import SelectField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError, InputRequired
from app.models import Student, Loan
from sqlalchemy import and_


class LoginForm(FlaskForm):  # pass in FlaskForm format
    username = StringField('Username', validators=[DataRequired()])  # set the validators
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

    def validate_username(self, username):  # self-def validators: query database for username.data to see if it's first
        if Student.query.filter_by(username=username.data).first():
            raise ValidationError('This username is already taken. Please choose another')

    def validate_email(self, email):
        if Student.query.filter_by(email=email.data).first():
            raise ValidationError('This email address is already registered. Please choose another')


class RemvStudentForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Remove Student')

    def validate_username(self, username):  # query database for username.data to see if there's None
        if not Student.query.filter_by(username=username.data).first():
            raise ValidationError('This username does not exist')


class BorrowForm(FlaskForm):
    student_id = StringField('Student ID', validators=[DataRequired()])
    device_id = StringField('Device ID', validators=[DataRequired()])
    submit = SubmitField('Borrow Device')

    def validate_student_id(self, student_id):
        if not student_id.data.isnumeric():  # simply check if student_id.data.isnumeric()
            raise ValidationError('This must be a positive integer')
        if not Student.query.get(student_id.data):  # get() specifically designed for primary key lookups
            raise ValidationError('There is no student with this id in the system')
        if Loan.query.filter(
                    (Loan.student_id == student_id.data)  # check if this student_id is on Loan table, and no returntime
                    &
                    (Loan.returndatetime.is_(None))  # filter(Table_name.column_name == value).first()
                ).first():
            raise ValidationError('This student cannot borrow another item until the previous loan has been returned')

    def validate_device_id(self, device_id):
        if not device_id.data.isnumeric():
            raise ValidationError('This must be a positive integer')
        if Loan.query.filter_by(device_id=device_id.data, returndatetime=None).first():
            raise ValidationError('This device cannot be borrowed as it is currently on loan')


class ReturnForm(FlaskForm):
    device_id = StringField('Device ID', validators=[DataRequired()])
    submit = SubmitField('Return Device')

    def validate_device_id(self, device_id):
        if not device_id.data.isnumeric():
            raise ValidationError('This must be a positive integer')
        if not Loan.query.filter_by(device_id=device_id.data, returndatetime=None).first():  # filter_by(column_name=value).first()
            raise ValidationError('This device is not exist or already returned')


class ReportForm(FlaskForm):
    report_type = SelectField('Report Type', choices=[('student', 'Student'), ('device', 'Device')],  # 'student', 'device' submitted value.data
                              validators=[DataRequired()])
    input_id = StringField('ID', validators=[InputRequired()])
    submit = SubmitField('Report')

    def validate_input_id(self, input_id):  # self refers to the instance of the class, which contains all attributes of the class
        report_type = self.report_type.data  # store report_type.data for use
        print(f"report type is: \n{report_type}")  # display in Flask server log
        if report_type == 'student':

            if not self.input_id.data.isnumeric():
                raise ValidationError('This must be a positive integer')
            if not Student.query.get(input_id.data):
                raise ValidationError('There is no student with this id in the system')
        else:
            if not self.input_id.data.isnumeric():
                raise ValidationError('This must be a positive integer')
