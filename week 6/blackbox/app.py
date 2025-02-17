from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

class Student(db.Model):
    student_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    roll_number = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String)

class Course(db.Model):
    course_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_code = db.Column(db.String, unique=True, nullable=False)
    course_name = db.Column(db.String, nullable=False)
    course_description = db.Column(db.String)

class Enrollment(db.Model):
    enrollment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.course_id'), nullable=False)

def create_tables():
    with app.app_context():
        db.create_all()

@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)

@app.route('/student/create', methods=['GET', 'POST'])
def create_student():
    if request.method == 'POST':
        roll = request.form['roll']
        f_name = request.form['f_name']
        l_name = request.form['l_name']
        courses = request.form.getlist('courses')

        if Student.query.filter_by(roll_number=roll).first():
            return render_template('already_exists.html')

        new_student = Student(roll_number=roll, first_name=f_name, last_name=l_name)
        db.session.add(new_student)
        db.session.commit()

        for course in courses:
            course_id = int(course.split('_')[1])  # Assuming course_1, course_2, etc.
            new_enrollment = Enrollment(student_id=new_student.student_id, course_id=course_id)
            db.session.add(new_enrollment)

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('create_student.html')

@app.route('/student/<int:student_id>/update', methods=['GET', 'POST'])
def update_student(student_id):
    student = Student.query.get_or_404(student_id)

    if request.method == 'POST':
        student.first_name = request.form['f_name']
        student.last_name = request.form['l_name']
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('update_student.html', student=student)

@app.route('/student/<int:student_id>/delete')
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/student/<int:student_id>')
def student_details(student_id):
    student = Student.query.get_or_404(student_id)
    enrollments = db.session.query(Enrollment, Course).join(Course).filter(Enrollment.student_id == student_id).all()
    return render_template('student_details.html', student=student, enrollments=enrollments)

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)