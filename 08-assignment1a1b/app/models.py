from app import db


class Student(db.Model):
    __tablename__ = 'students'
    student_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    username = db.Column(db.String(20), nullable=False, unique=True, index=True)
    firstname = db.Column(db.String(32))
    lastname = db.Column(db.String(32), nullable=False, index=True)
    email = db.Column(db.String(64), nullable=False, unique=True, index=True)
    loans = db.relationship('Loan', backref='student', lazy='dynamic')
    # 1a
    active = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return (f"student(student_id='{self.student_id}', username='{self.username}', lastname='{self.lastname}',"
                f"firstname='{self.firstname}' , email='{self.email}', active='{self.active}')")


class Loan(db.Model):
    __tablename__ = 'loans'
    loan_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    device_id = db.Column(db.Integer, nullable=False)
    borrowdatetime = db.Column(db.DateTime, nullable=False)
    returndatetime = db.Column(db.DateTime, nullable=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)
    # 1b
    damaged = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return (f"loan(loan_id='{self.loan_id}', device_id='{self.device_id}', "
                f"borrowdatetime='{self.borrowdatetime}' , returndatetime='{self.returndatetime}', "
                f"damaged='{self.damaged}', student='{self.student}')")


