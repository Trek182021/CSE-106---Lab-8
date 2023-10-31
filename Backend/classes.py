from flask import flash
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


db = SQLAlchemy()
admin = Admin()

student_course_grade = db.Table(
    'student_course_grade',
    db.Column('student_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id')),
    db.Column('grade', db.Integer)
)

class RolesUsers(db.Model):
    __tablename__="roles_users"
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))

class CourseGrade(db.Model):
    __tablename__ = 'course_grade'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    grade = db.Column(db.Float)
    
    user = db.relationship("User", back_populates="coursegrades_user")
    course = db.relationship("Course", back_populates="coursegrades_course")
    
    def __repr__(self):
        return f'UserId: {self.user_id}, CourseId: {self.course_id}, Grade: {self.grade}'
    

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    # teacher = db.Column(db.Integer, db.ForeignKey('user.id'))
    teacher_id = db.Column(db.ForeignKey('user.id'))
    teacher = db.relationship("User", back_populates="teacherCourses")
    time = db.Column(db.Text)
    capacity = db.Column(db.Integer)
    coursegrades_course = db.relationship("CourseGrade", back_populates="course")
    
    def __repr__(self):
        return f'{self.name}'
    def __str__(self):
        return self.name
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    # role = db.Column(db.Integer, db.ForeignKey('role.id'))
    role_id = db.Column(db.ForeignKey('role.id'), nullable=False)
    role = db.relationship("Role", back_populates="users")
    teacherCourses = db.relationship("Course", back_populates="teacher")
    courses = db.relationship('Course', secondary=student_course_grade, backref='users')
    coursegrades_user = db.relationship("CourseGrade", back_populates="user")
    
    def __str__(self):
        return self.name
    def __repr__(self):
        return f'<User {self.name}>'
    def serialize(self):
        return {'name': self.name, 'grade': self.grade}
    def isTeacher(self):
        return self.role_id == 2;
    
class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    users = db.relationship("User", back_populates="role")
    
    def __str__(self):
        return self.name
    def __repr__(self):
        return f'<User {self.name}>'

class RoleView(ModelView):
    form_columns=["name", "description"]
    column_list=["name", "description", "users"]
    
class UserView(ModelView):
    form_columns = ['name', 'username', 'password', 'role']
    column_list= ['username', 'role', 'courses']
    
class CourseView(ModelView):
    form_columns=['name', 'teacher', 'time', 'capacity']
    column_list=['name', 'teacher', 'time', 'capacity']
    form_args = {
        'teacher': {
            'query_factory': lambda: User.query.filter_by(role_id=2),
        }
    }
    def validate_form_on_submit(self, form):
        course = db.Query(Course).filter_by(name=form.name.data).first()
        if (course):
            flash("Error: Course already exists.")
    
class CourseGradeView(ModelView):
    form_columns = ["user", "course", "grade"]
    column_list = ['user', 'course', 'grade']
    form_args = {
        'user': {
            'query_factory': lambda: User.query.filter_by(role_id=1),
        }
    }
    
    def after_model_change(self, form, model, is_created):
        try:
            newGrade = 0 if form.grade.data == None else float(form.grade.data)
            statement = student_course_grade.insert().values(student_id=int(form.user.data.id), course_id=int(form.course.data.id), grade=newGrade)
            db.session.execute(statement)
            db.session.commit()
        except:
            print("ERROR!!!!!")
            
    def validate_form_on_submit(self, form):
        print(form)
        test = db.Query(CourseGrade).filter_by(user_id=form.user.data.id, course_id=form.course.data.id).first()
        if (test):
            flash("Error: Student Grade already exists.")
            
                      
admin.add_view(CourseGradeView(CourseGrade, db.session))
admin.add_view(RoleView(Role, db.session))
admin.add_view(CourseView(Course, db.session))
admin.add_view(UserView(User, db.session))