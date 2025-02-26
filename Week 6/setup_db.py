from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///api_database.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Models
class Course(db.Model):
    __tablename__ = 'course'
    course_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_name = db.Column(db.String, nullable=False)
    course_code = db.Column(db.String, unique=True, nullable=False)
    course_description = db.Column(db.String)

class Student(db.Model):
    __tablename__ = 'student'
    student_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    roll_number = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String)

class Enrollment(db.Model):
    __tablename__ = 'enrollment'
    enrollment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.course_id'), nullable=False)

# Create the database and tables
with app.app_context():
    db.create_all()

    # Add sample courses
    course1 = Course(course_name="Mathematics", course_code="MA101", course_description="Introduction to Mathematics")
    course2 = Course(course_name="Physics", course_code="PH101", course_description="Introduction to Physics")
    db.session.add_all([course1, course2])

    # Add sample students
    student1 = Student(roll_number="S1001", first_name="John", last_name="Doe")
    student2 = Student(roll_number="S1002", first_name="Jane", last_name="Smith")
    db.session.add_all([student1, student2])

    # Add sample enrollments
    enrollment1 = Enrollment(student_id=1, course_id=1)  # John Doe enrolled in Mathematics
    enrollment2 = Enrollment(student_id=2, course_id=2)  # Jane Smith enrolled in Physics
    db.session.add_all([enrollment1, enrollment2])

    # Commit changes
    db.session.commit()

print("Database created and populated successfully!")