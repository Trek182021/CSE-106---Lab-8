from flask import Flask, jsonify, request, flash, redirect, url_for
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import func, text
from flask_login import current_user, login_user
# import get_routes


# cors = CORS(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3'
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3'
app.config["SECRET_KEY"] = 'mysecret'



db = SQLAlchemy(app)
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
    
class User(db.Model):
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
    def check_password(self, password):
        return self.password == password
    
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


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.secret_key = 'keep it secret, keep it safe'

@login_manager.user_loader
def load_user(user_id):
    return User.get_id(user_id)

@app.route('/signin', methods= ['POST'])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.query.filter_by(username=request.json['username']).first()
    if user is None or not user.check_password(request.json['password']):
        return redirect(url_for('login'))
    login_user(user)
    return redirect(url_for('index'))

@app.route('/studentCourses/<int:id_>', methods=['GET'])
def getStudentCourses(id_):
    res = []
    enrolledNum = db.session.query(CourseGrade.course_id.label('id'), func.count().label('num')).group_by('course_id').subquery()
    studentCourses = db.session.query(Course.name, User.name, Course.time, enrolledNum.c.num, Course.capacity).join(User).join(enrolledNum).filter(CourseGrade.course_id == Course.id, Course.teacher_id == User.id, CourseGrade.course_id == enrolledNum.c.id, CourseGrade.user_id == id_).all()
    for i in studentCourses:
        res.append({'Course': i[0], 'Teacher': i[1], 'Time': i[2], 'EnrolledNum': i[3], 'Capacity': i[4]})

    return jsonify(res)

@app.route('/courses', methods=['GET'])
def getCourses():
    res = []
    query = text('SELECT course.name as courseName, user.name as teacher, course.time as time, (course.capacity) as capacity, CASE when c2.enrolledNum THEN c2.enrolledNum ELSE 0 END as enrolledNum FROM course, user  LEFT JOIN ( SELECT course_id, count(*) as enrolledNum FROM course_grade cg GROUP BY cg.course_id ) c2 ON c2.course_id = course.id WHERE course.teacher_id = user.id')
    with db.engine.connect() as conn:
        response = conn.execute(query)
        for i in response:
            res.append({'Course': i[0], 'Teacher': i[1], 'Time': i[2], 'Capacity': i[3], 'EnrolledNum': i[4]})
    return jsonify(res)

@app.route('/courses/<int:course_id>', methods=['GET'])
def getStudents(course_id):
    res = []
    query = text('SELECT user.name, course_grade.grade FROM course, course_grade, user WHERE course.id = course_grade.course_id AND course_grade.user_id = user.id AND course.id = :course_id;')
    with db.engine.connect() as conn:
        response = conn.execute(query, {'course_id': course_id})
        for i in response:
            res.append({'Student': i[0], 'Grade': i[1]})
    return jsonify(res)

@app.route('/teacherCourses/<int:teacher_id>', methods=['GET'])
def getTeacherCourses(teacher_id):
    res = []
    query = text('SELECT course.name, user.name, course.time, CASE when c2.enrolledNum THEN c2.enrolledNum ELSE 0 END as enrolledNum,  course.capacity FROM course, user LEFT JOIN ( SELECT course_id, count(*) as enrolledNum FROM course_grade cg GROUP BY cg.course_id ) c2 ON c2.course_id = course.id WHERE course.teacher_id = :teacher_id AND course.teacher_id = user.id;')
    with db.engine.connect() as conn:
        response = conn.execute(query, {'teacher_id': teacher_id})
        for i in response:
            res.append({'Course': i[0], 'Teacher': i[1], 'Time': i[2], 'EnrolledNum': i[3], 'Capacity': i[4]})
    return jsonify(res)
    

@app.route('/signup/<int:course_id>', methods=['POST'])
def courseSignup(course_id):
    print("COURSE ID", course_id)
    data = request.get_json()
    print(data)
    insertToCourseGrade = text("INSERT INTO course_grade (user_id, course_id, grade) VALUES (:user_id, :course_id, :grade);")
    insertToStudentCourseGrade = text("INSERT INTO student_course_grade (student_id, course_id, grade) VALUES (:user_id, :course_id, :grade);")
    with db.engine.connect() as conn:
        conn.execute(insertToCourseGrade, {'course_id': course_id, 'grade': data['grade'], 'user_id': data['user_id']})
        conn.execute(insertToStudentCourseGrade, {'course_id': course_id, 'grade': data['grade'], 'user_id': data['user_id']})
        conn.commit()
    return data

@app.route('/grades/<int:course_id>', methods=['PUT'])
def updateGrade(course_id):
    data = request.get_json()
    query = text('UPDATE course_grade SET grade = :grade WHERE course_grade.course_id = :course_id AND course_grade.user_id = :user_id;')
    with db.engine.connect() as conn:
        conn.execute(query, {'grade': data['grade'], 'course_id': course_id, 'user_id': data['user_id']})
        conn.commit()
    return "200"

# db.init_app(app)
admin.init_app(app)
    
if __name__ == '__main__':
    app.run()
    
