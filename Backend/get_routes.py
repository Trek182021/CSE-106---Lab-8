from __main__ import app, db, User, Course, CourseGrade, Role
from flask import Flask, jsonify, request

'''
*************
Login/Logout using JWT
*************

*************
GET /studentCourses/:student_id - get all courses for a specific student

QUERY:
`
"""
SELECT course.name AS course_name, user.name AS user_name, course.time AS course_time, anon_1.num AS anon_1_num, course.capacity AS course_capacity 
FROM course JOIN user ON user.id = course.teacher_id JOIN (SELECT course_grade.course_id AS id, count(*) AS num
FROM course_grade GROUP BY course_grade.course_id) AS anon_1 ON course.id = anon_1.id, course_grade
WHERE course_grade.course_id = course.id AND course.teacher_id = user.id AND course_grade.course_id = anon_1.id AND course_grade.user_id = ?
""";
`
*************

'''

@app.route('/studentCourses/<int:id>', method=['GET'])
def getStudentCourses(id):
    query = """
            SELECT c1.name as courseName, user.name as teacher, c1.time as time, c2.enrolledNum, (c1.capacity) as capacity
            FROM course_grade, course c1, user,
            ( SELECT course_id, count(*) as enrolledNum FROM course_grade GROUP BY course_grade.course_id ) c2
            WHERE course_grade.course_id = c1.id AND c1.teacher_id = user.id AND course_grade.course_id = c2.course_id
            AND course_grade.user_id = ?;
            """
    studentCourses = db.session.query(query, id);
    return jsonify(studentCourses)
    
'''
*************
GET /courses - get all courses with all info + capacity

QUERY:
`
SELECT course.name as courseName, user.name as teacher, course.time as time, (course.capacity) as capacity, 
CASE when c2.enrolledNum THEN c2.enrolledNum ELSE 0 END as enrolledNum
FROM course, user 
LEFT JOIN 
( SELECT course_id, count(*) as enrolledNum FROM course_grade cg GROUP BY cg.course_id ) c2 ON c2.course_id = course.id
WHERE course.teacher_id = user.id;
`
*************

*************
POST /signup/:course_id - add CourseGrade to student and course
`
INSERT INTO course_grade (user_id, course_id, grade) VALUES (?, ?, ?);
INSERT INTO student_course_grade (student_id, course_id, grade) VALUES (?, ?, ?);
`
*************

*************
GET /teacherCourses/:teacher_id - get all courses that a teacher teaches
`
SELECT course.name, user.name, course.time, 
CASE when c2.enrolledNum THEN c2.enrolledNum ELSE 0 END as enrolledNum, 
course.capacity FROM course, user LEFT JOIN 
( SELECT course_id, count(*) as enrolledNum FROM course_grade cg GROUP BY cg.course_id ) c2 ON c2.course_id = course.id
WHERE course.teacher_id = ? AND course.teacher_id = user.id;
`
*************

*************
GET /courseStudents/:course_id - get all students in enrolled in a course + their grade
`
SELECT user.name, course_grade.grade FROM course, course_grade, user
WHERE course.id = course_grade.course_id AND course_grade.user_id = user.id AND course.id = ?;
`
*************

*************
POST /grade/:course_id - Edits a student grade
`
UPDATE course_grade
SET grade = ?
WHERE course_grade.id = ? AND course_grade.user_id = ?;
`
*************
'''


@app.route('/grades', methods=['GET', 'POST'])
def grades():
    if request.method == 'GET':
        users= Student.query.all()
        return jsonify([e.serialize() for e in users])
    if request.method == 'POST':
        res = request.get_json()
        studentName = res['name']
        newGrade = res['grade']
        newUser = Student(name=studentName, grade=newGrade)
        db.session.add(newUser)
        db.session.commit()
        return "SUCCESS"

@app.route('/grades/<studentName>', methods = ['GET', 'PUT', "DELETE"])
def grade(studentName):
    studentName.replace('%20', ' ')
    user = User.query.filter_by(name=studentName).first()
    if request.method == 'GET':
        return user.serialize()
    if request.method == 'PUT':
        res = request.get_json()
        newGrade = res['grade']
        user.grade = newGrade
        db.session.add(user)
        db.session.commit()    
        return "200"
    if request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return "200"

