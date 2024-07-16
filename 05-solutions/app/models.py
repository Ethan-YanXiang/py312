from app import db
# from package app import db: SQLAlchemy(app)


class Student(db.Model):  # models classes inherit from 'db.Model'
    __tablename__ = 'students'
    student_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)  # if primary_key=True, then (unique=True, nullable=False)
    username = db.Column(db.String(20), nullable=False, unique=True, index=True)  # and SQLAlchemy just make it autoIncremnet if (db.Integer, primary_key=True)
    firstname = db.Column(db.String(32))
    lastname = db.Column(db.String(32), nullable=False, index=True)
    email = db.Column(db.String(64), nullable=False, unique=True, index=True)
    loans = db.relationship('Loan', backref='student', lazy='dynamic', cascade='all,delete')
    # a virtual field in the Loan class, when the repr in Loan print out self.student, print the repr in Student object

    def __repr__(self):
        return f"student('{self.username}', '{self.lastname}', '{self.firstname}' , '{self.email}')"
        # for an object, __repr__ generates the string representation the way we want in Flask server log


class Loan(db.Model):
    __tablename__ = 'loans'
    loan_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    device_id = db.Column(db.Integer, nullable=False)
    borrowdatetime = db.Column(db.DateTime, nullable=False)
    returndatetime = db.Column(db.DateTime, nullable=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)
    # an actual student_id attribute to identify who make the loan

    def __repr__(self):
        return f"loan('{self.device_id}', '{self.borrowdatetime}' , '{self.returndatetime}', '{self.student}')"
