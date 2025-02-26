from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///api_database.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)

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

# Error Handling
def error_response(error_code, error_message, status_code=400):
    return jsonify({"error_code": error_code, "error_message": error_message}), status_code

# Course APIs
class CourseAPI(Resource):
    def get(self, course_id=None):
        if course_id:
            course = Course.query.get(course_id)
            if not course:
                return {"message": "Course not found"}, 404
            return {
                "course_id": course.course_id,
                "course_name": course.course_name,
                "course_code": course.course_code,
                "course_description": course.course_description
            }, 200
        else:
            courses = Course.query.all()
            return [{
                "course_id": course.course_id,
                "course_name": course.course_name,
                "course_code": course.course_code,
                "course_description": course.course_description
            } for course in courses], 200

    def post(self):
        data = request.get_json()
        # Validate required fields
        if not data.get("course_name"):
            return error_response("COURSE001", "Course Name is required")
        if not data.get("course_code"):
            return error_response("COURSE002", "Course Code is required")
        try:
            new_course = Course(
                course_name=data["course_name"],
                course_code=data["course_code"],
                course_description=data.get("course_description")
            )
            db.session.add(new_course)
            db.session.commit()
            return {
                "course_id": new_course.course_id,
                "course_name": new_course.course_name,
                "course_code": new_course.course_code,
                "course_description": new_course.course_description
            }, 201
        except IntegrityError:
            db.session.rollback()
            return error_response("COURSE003", "Course Code already exists", 409)

    def put(self, course_id):
        course = Course.query.get(course_id)
        if not course:
            return {"message": "Course not found"}, 404
        data = request.get_json()
        course.course_name = data.get("course_name", course.course_name)
        course.course_code = data.get("course_code", course.course_code)
        course.course_description = data.get("course_description", course.course_description)
        db.session.commit()
        return {
            "course_id": course.course_id,
            "course_name": course.course_name,
            "course_code": course.course_code,
            "course_description": course.course_description
        }, 200

    def delete(self, course_id):
        course = Course.query.get(course_id)
        if not course:
            return {"message": "Course not found"}, 404
        db.session.delete(course)
        db.session.commit()
        return {"message": "Successfully Deleted"}, 200

# Student APIs
class StudentAPI(Resource):
    def get(self, student_id=None):
        if student_id:
            student = Student.query.get(student_id)
            if not student:
                return {"message": "Student not found"}, 404
            return {
                "student_id": student.student_id,
                "roll_number": student.roll_number,
                "first_name": student.first_name,
                "last_name": student.last_name
            }, 200
        else:
            students = Student.query.all()
            return [{
                "student_id": student.student_id,
                "roll_number": student.roll_number,
                "first_name": student.first_name,
                "last_name": student.last_name
            } for student in students], 200

    def post(self):
        data = request.get_json()
        # Validate required fields
        if not data.get("roll_number"):
            return error_response("STUDENT001", "Roll Number is required")
        if not data.get("first_name"):
            return error_response("STUDENT002", "First Name is required")
        try:
            new_student = Student(
                roll_number=data["roll_number"],
                first_name=data["first_name"],
                last_name=data.get("last_name")
            )
            db.session.add(new_student)
            db.session.commit()
            return {
                "student_id": new_student.student_id,
                "roll_number": new_student.roll_number,
                "first_name": new_student.first_name,
                "last_name": new_student.last_name
            }, 201
        except IntegrityError:
            db.session.rollback()
            return error_response("STUDENT003", "Roll Number already exists", 409)

    def put(self, student_id):
        student = Student.query.get(student_id)
        if not student:
            return {"message": "Student not found"}, 404
        data = request.get_json()
        student.roll_number = data.get("roll_number", student.roll_number)
        student.first_name = data.get("first_name", student.first_name)
        student.last_name = data.get("last_name", student.last_name)
        db.session.commit()
        return {
            "student_id": student.student_id,
            "roll_number": student.roll_number,
            "first_name": student.first_name,
            "last_name": student.last_name
        }, 200

    def delete(self, student_id):
        student = Student.query.get(student_id)
        if not student:
            return {"message": "Student not found"}, 404
        db.session.delete(student)
        db.session.commit()
        return {"message": "Successfully Deleted"}, 200

# Enrollment APIs
class EnrollmentAPI(Resource):
    def get(self, student_id):
        student = Student.query.get(student_id)
        if not student:
            return error_response("ENROLLMENT002", "Student does not exist")
        enrollments = Enrollment.query.filter_by(student_id=student_id).all()
        if not enrollments:
            return {"message": "Student is not enrolled in any course"}, 404
        return [{
            "enrollment_id": enrollment.enrollment_id,
            "student_id": enrollment.student_id,
            "course_id": enrollment.course_id
        } for enrollment in enrollments], 200

    def post(self, student_id):
        student = Student.query.get(student_id)
        if not student:
            return error_response("ENROLLMENT002", "Student does not exist")
        data = request.get_json()
        course = Course.query.get(data.get("course_id"))
        if not course:
            return error_response("ENROLLMENT001", "Course does not exist")
        try:
            new_enrollment = Enrollment(student_id=student_id, course_id=course.course_id)
            db.session.add(new_enrollment)
            db.session.commit()
            return {
                "enrollment_id": new_enrollment.enrollment_id,
                "student_id": new_enrollment.student_id,
                "course_id": new_enrollment.course_id
            }, 201
        except IntegrityError:
            db.session.rollback()
            return error_response("ENROLLMENT003", "Enrollment already exists")

class EnrollmentDeleteAPI(Resource):
    def delete(self, student_id, course_id):
        student = Student.query.get(student_id)
        if not student:
            return error_response("ENROLLMENT002", "Student does not exist")
        course = Course.query.get(course_id)
        if not course:
            return error_response("ENROLLMENT001", "Course does not exist")
        enrollment = Enrollment.query.filter_by(student_id=student_id, course_id=course_id).first()
        if not enrollment:
            return {"message": "Enrollment for the student not found"}, 404
        db.session.delete(enrollment)
        db.session.commit()
        return {"message": "Successfully Deleted"}, 200

# Add Resources to API
api.add_resource(CourseAPI, "/api/course", "/api/course/<int:course_id>")
api.add_resource(StudentAPI, "/api/student", "/api/student/<int:student_id>")
api.add_resource(EnrollmentAPI, "/api/student/<int:student_id>/course")
api.add_resource(EnrollmentDeleteAPI, "/api/student/<int:student_id>/course/<int:course_id>")

if __name__ == '__main__':
    app.run(debug=True)