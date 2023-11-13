from flask import jsonify, request, redirect, url_for
from sqlalchemy import func, text
from flask import Blueprint
from app import db
from classes import CourseGrade, Course, User

api = Blueprint('api',__name__)

@api.route('/studentCourses/<int:id_>', methods=['GET'])
def getStudentCourses(id_):
    res = []
    enrolledNum = db.session.query(CourseGrade.course_id.label('id'), func.count().label('num')).group_by('course_id').subquery()
    studentCourses = db.session.query(Course.name, User.name, Course.time, enrolledNum.c.num, Course.capacity).join(User).join(enrolledNum).filter(CourseGrade.course_id == Course.id, Course.teacher_id == User.id, CourseGrade.course_id == enrolledNum.c.id, CourseGrade.user_id == id_).all()
    for i in studentCourses:
        res.append({'Course': i[0], 'Teacher': i[1], 'Time': i[2], 'EnrolledNum': i[3], 'Capacity': i[4]})
    return jsonify(res)

@api.route('/courses/<int:student_id>', methods=['GET'])
def getCourses(student_id):
    res = []
    query = text('SELECT course.id, course.name as courseName, user.name as teacher, course.time as time, (course.capacity) as capacity, CASE WHEN c2.enrolledNum THEN c2.enrolledNum ELSE 0 END as enrolledNum, CASE WHEN cg.u_id != 0 THEN 1 ELSE 0 END as isSignedUp FROM course, user LEFT JOIN ( SELECT course_id, count(*) as enrolledNum FROM course_grade cg GROUP BY cg.course_id ) c2 ON c2.course_id = course.id LEFT JOIN ( SELECT course_id as id, user_id as u_id FROM course_grade WHERE user_id = :_user_id ) cg ON cg.id = course_id WHERE course.teacher_id = user.id')
    with db.engine.connect() as conn:
        response = conn.execute(query, {'_user_id': student_id})
        for i in response:
            res.append({'id': i[0], 'Course': i[1], 'Teacher': i[2], 'Time': i[3], 'Capacity': i[4], 'EnrolledNum': i[5], 'IsSignedUp': i[6]})
    return jsonify(res)

@api.route('/signup/<int:course_id>', methods=['POST', 'DELETE'])
def courseSignup(course_id):
    print("COURSE ID", course_id)
    
    if request.method == 'POST':
        curr_course = course_id
        _user_id = request.form.get('user_id')
        if (CourseGrade.query.filter_by(user_id=_user_id, course_id=curr_course) is not None):
            print(_user_id, course_id, "NUKLL")
            insertToCourseGrade = text("INSERT INTO course_grade (user_id, course_id, grade) VALUES (:user_id, :course_id, :grade);")
            insertToStudentCourseGrade = text("INSERT INTO student_course_grade (student_id, course_id, grade) VALUES (:user_id, :course_id, :grade);")
            with db.engine.connect() as conn:
                conn.execute(insertToCourseGrade, {'course_id': course_id, 'grade': 0, 'user_id': _user_id})
                conn.execute(insertToStudentCourseGrade, {'course_id': course_id, 'grade': 0, 'user_id': _user_id})
                conn.commit()
            return redirect(url_for('studentsPage'))
        else:
            return redirect(url_for('studentsPage'))

@api.route('/drop/<int:course_id>', methods=['POST'])
def courseDrop(course_id):
    print("COURSE ID", course_id)
    
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        deleteCourseGrade = text("DELETE FROM course_grade WHERE course_id = :_course_id AND user_id = :_user_id")
        deleteStudentCourseGrade = text("DELETE FROM student_course_grade WHERE student_id = :_student_id and course_id = :_course_id")
        with db.engine.connect() as conn:
            conn.execute(deleteCourseGrade, {'_course_id': course_id, '_user_id': user_id})
            conn.execute(deleteStudentCourseGrade, {'_course_id': course_id, '_student_id': user_id})
            conn.commit()
        return redirect(url_for('studentsPage'))
       

@api.route('/courseGrade/<int:course_id>', methods=['GET'])
def getStudents(course_id):
    res = []
    query = text('SELECT u2.name, u1.name, course_grade.grade, u1.id FROM course, course_grade, user u1, user u2 WHERE course.teacher_id = u2.id AND course.id = course_grade.course_id AND course_grade.user_id = u1.id AND course.id = :course_id;')
    with db.engine.connect() as conn:
        response = conn.execute(query, {'course_id': course_id})
        for i in response:
            res.append({'Teacher': i[0], 'Student': i[1], 'Grade': i[2], 'Student_Id': i[3]})
    return jsonify(res)

@api.route('/teacherCourses/<int:teacher_id>', methods=['GET'])
def getTeacherCourses(teacher_id):
    res = []
    query = text('SELECT course.name, user.name, course.time, CASE when c2.enrolledNum THEN c2.enrolledNum ELSE 0 END as enrolledNum,  course.capacity, course.id FROM course, user LEFT JOIN ( SELECT course_id, count(*) as enrolledNum FROM course_grade cg GROUP BY cg.course_id ) c2 ON c2.course_id = course.id WHERE course.teacher_id = :teacher_id AND course.teacher_id = user.id;')
    with db.engine.connect() as conn:
        response = conn.execute(query, {'teacher_id': teacher_id})
        for i in response:
            res.append({'Course': i[0], 'Teacher': i[1], 'Time': i[2], 'EnrolledNum': i[3], 'Capacity': i[4], 'id': i[5]})
    return jsonify(res)

@api.route('/grades/<int:course_id>', methods=['PUT'])
def updateGrade(course_id):
    data = request.get_json()
    query = text('UPDATE course_grade SET grade = :grade WHERE course_grade.course_id = :course_id AND course_grade.user_id = :user_id;')
    with db.engine.connect() as conn:
        conn.execute(query, {'grade': data['grade'], 'course_id': course_id, 'user_id': data['user_id']})
        conn.commit()
    return "200"

@api.route('/course/<int:course_id>', methods=['GET'])
def getCourse(course_id):
    query = text("SELECT * FROM course WHERE id = :course_id")
    res = []
    with db.engine.connect() as conn:
        response = conn.execute(query, {'course_id': course_id})
        for i in response:
            res.append({'id': i[0], 'Course': i[1], 'teacher_id': i[2], 'Time': i[3], 'Capacity': i[4]})
    return jsonify(res)