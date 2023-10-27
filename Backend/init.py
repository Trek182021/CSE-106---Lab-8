from app import db, User, Course, Role

db.create_all()

user1 = User(name='A',username='a1',password='a1')
user2 = User(name='B',username='b1',password='b1')
user3 = User(name='C',username='c1',password='c1')

role1 = Role(name='Student',description='role for students')
role2 = Role(name='Teacher',description='role for teacher')



course1 = Course(name='ENGR 151',time='TR 11:00-11:50AM')
course2= Course(name='CS 106',time='TR 05:00-06:00PM')
course3= Course(name='ME 185',time='MW 01:00-04:00PM')




db.session.add_all([user1, user2, user3])
db.session.add_all([role1, role2])
db.session.add_all([course1, course2, course3])

db.session.commit()
statement = student_course_grade.insert().values(student_id=1, course_id=1, grade=92.2)
statement2 = student_course_grade.insert().values(student_id=1, course_id=2, grade=94.5)
statement3 = student_course_grade.insert().values(student_id=2, course_id=2, grade=99.99)
statement4= student_course_grade.insert().values(student_id=1, course_id=3, grade=75)
user1 = User.query.filter_by(id=1).first()
user1.role = 1
user2 = User.query.filter_by(id=2).first()
user2.role = 2
user3 = User.query.filter_by(id=3).first()
user3.role = 1
db.session.commit()
course1= Course.query.filter_by(id=1).first()
course1.teacher = 2
course2= Course.query.filter_by(id=2).first()
course2.teacher = 2

course3= Course.query.filter_by(id=3).first()
course3.teacher = 2

c1 = CourseGrade(user_id=1, course_id=1, grade=92.2)
c2 = CourseGrade(user_id=1, course_id=2, grade=99.9)
c3 = CourseGrade(user_id=1, course_id=3, grade=72.5)
c4 = CourseGrade(user_id=2, course_id=2, grade=82.8)
c5 = CourseGrade(user_id=2, course_id=1, grade=91.6)
c6 = CourseGrade(user_id=3, course_id=1, grade=45.2)
db.session.add_all([c1,c2,c3,c4,c5])