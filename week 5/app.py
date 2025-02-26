from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    roll_number = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_code = db.Column(db.String, unique=True, nullable=False)
    course_name = db.Column(db.String, nullable=False)
    course_description = db.Column(db.String)

class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)

# Home Route
@app.route('/')
def home():
    students = Student.query.all()
    return render_template('index.html', students=students)

@app.route('/student/create', methods=['GET', 'POST'])
def create_student():
    if request.method == 'POST':
        roll = request.form['roll']
        f_name = request.form['f_name']
        l_name = request.form['l_name']
        courses_selected = request.form.getlist('courses')

        if Student.query.filter_by(roll_number=roll).first():
            return render_template('error.html', message='Roll Number already exists!')
        
        student = Student(roll_number=roll, first_name=f_name, last_name=l_name)
        db.session.add(student)
        db.session.commit()
        
        print(f"Selected courses: {courses_selected}")

        for course_id in courses_selected:
            course = Course.query.get(course_id)  
            if course:
                enrollment = Enrollment(student_id=student.id, course_id=int(course_id))
                db.session.add(enrollment)
                print(f"Enrolled student {student.roll_number} in course {course.course_code}")
            else:
                print(f"Course with ID {course_id} does not exist!")
        
        db.session.commit()  
        
        return redirect(url_for('home'))
    return render_template('add_student.html')

# Update Student Route
@app.route('/student/<int:student_id>/update', methods=['GET', 'POST'])
def update_student(student_id):
    student = Student.query.get_or_404(student_id)
    if request.method == 'POST':
        student.first_name = request.form['f_name']
        student.last_name = request.form['l_name']
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('update_student.html', student=student)

# Delete Student Route
@app.route('/student/<int:student_id>/delete')
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    Enrollment.query.filter_by(student_id=student.id).delete()
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/student/<int:student_id>')
def student_details(student_id):
    student = Student.query.get_or_404(student_id)
    enrollments = Enrollment.query.filter_by(student_id=student.id).all()
    print(f"Enrollments for student {student.roll_number}: {[e.course_id for e in enrollments]}")

    courses = []
    for enrollment in enrollments:
        course = Course.query.get(enrollment.course_id)
        if course:
            courses.append(course)
            print(f"Found course: {course.course_code}")
        else:
            print(f"Course with ID {enrollment.course_id} does not exist!")

    return render_template('student_details.html', student=student, courses=courses)

if __name__ == '__main__':
    app.run(debug=True)
