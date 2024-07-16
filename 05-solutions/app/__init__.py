import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = b'WR#&f&+%78er0we=%799eww+#7^90-;s'

basedir = os.path.abspath(os.path.dirname(__file__))  # using os to find the abspath of the running web app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data', 'data.sqlite')
# creating our database file by joining the web app and prefix 'sqlite:///'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # preventing getting error message
db = SQLAlchemy(app)  # all the interactions to the database are gonna come through this variable


from app import views
from app.models import *  # we need all the classes in app.models for the following steps


@app.shell_context_processor  # tell flask shell to import these variables to db.create_all(); db.session.commit()
def make_shell_context():
    return dict(db=db, Student=Student, Loan=Loan, datetime=datetime)
# db.drop_all() to delete the whole database
# l1 = Loan(device_id='1', borrowdatetime = datetime.now(), student=s1)
# l1.returndatetime=datetime.now()
# db.session.delete(s)

# db.session.add(l1)
# db.session.commit()
# print(l1.loan_id)

# db.session.rollback()

# Student.query.first(): Normally querying the model classes
# Student.query.all()

# Student.query.filter_by(lastname='Lin').all()
# Loan.query.filter_by(student=s1).all()

# s1:(class).loans:(attribute).all()
# l1 = s1.loans.first()
# l1.student():(repr attribute)

# do control + c in flask shell to terminate the old models.py and reopen db.create_all()
# 1.using flask shell to create database
# 2.accessing other fields in forms1.py validators
