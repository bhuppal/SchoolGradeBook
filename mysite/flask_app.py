# A very simple Flask Hello World app for you to get started with...
from datetime import datetime
from flask import Flask, redirect, render_template, request, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import login_user, LoginManager, UserMixin, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
from flask_session import Session
import json


app = Flask(__name__)

app.config["DEBUG"] = True
app.config['TESTING'] = False

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="SchoolGradeBook",
    password="Saibaba123!",
    hostname="SchoolGradeBook.mysql.pythonanywhere-services.com",
    databasename="SchoolGradeBook$schoolgradebook",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


app.secret_key = "SchoolGradeBook"
login_manager = LoginManager()
login_manager.init_app(app)

def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d")]

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    instructor = db.relationship('Instructor', backref='User', uselist=False)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username

class Instructor(db.Model):
    __tablename__ = "sgb_Instructor"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    title = db.Column(db.String(10))
    position  = db.Column(db.String(50))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    notes = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique = True)
    courses = db.relationship('Course', backref='course_instructor')


    def json(self):
        return {
                'id': self.id,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'title': self.title,
                'position': self.position,
                'email': self.email,
                'phone': self.phone,
                'notes': self.notes,
                'user_id': self.user_id
        }


    def get_all_instructors():
        return [Instructor.json(instructor) for instructor in Instructor.query.all()]

    def __repr__(self):
        instructor_object = {
                'id': self.id,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'title': self.title,
                'position': self.position,
                'email': self.email,
                'phone': self.phone,
                'notes': self.notes,
                'user_id': self.user_id
        }
        return json.dumps(instructor_object)


class Course(db.Model):
    __tablename__ = "sgb_Course"

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.String(150))
    course_name = db.Column(db.String(150))
    course_description = db.Column(db.String(4000))
    course_schedule = db.Column(db.String(200))
    course_startdate = db.Column(db.DateTime)
    course_enddate = db.Column(db.DateTime)
    instructor_id = db.Column(db.Integer, db.ForeignKey('sgb_Instructor.id'))
    assignments = db.relationship('Assignment', backref='course_assignment')

    def json(self):
        return {
                'id': self.id,
                'course_id': self.course_id,
                'course_name': self.course_name,
                'course_description': self.course_description,
                'course_schedule': self.course_schedule,
                'course_startdate': dump_datetime(self.course_startdate),
                'course_enddate': dump_datetime(self.course_enddate)
        }


    def get_all_courses():
        return [Course.json(course) for course in Course.query.all()]

    def __repr__(self):
        Course_object = {
                 'id': self.id,
                'course_id': self.course_id,
                'course_name': self.course_name,
                'course_description': self.course_description,
                'course_schedule': self.course_schedule,
                'course_startdate': dump_datetime(self.course_startdate),
                'course_enddate': dump_datetime(self.course_enddate)
        }
        return json.dumps(Course_object)


class Assignment(db.Model):
    __tablename__ = "sgb_Assignment"

    id = db.Column(db.Integer, primary_key=True)
    assignment_name = db.Column(db.String(150))
    assignment_startdate = db.Column(db.DateTime)
    assignment_duedate = db.Column(db.DateTime)
    assignment_grade = db.Column(db.Integer)
    courses = db.Column(db.Integer, db.ForeignKey('sgb_Course.id'))


    def json(self):
        return {
                'id': self.id,
                'assignment_name': self.assignment_name,
                'assignment_startdate': dump_datetime(self.assignment_startdate),
                'assignment_duedate': dump_datetime(self.assignment_duedate),
                'assignment_grade': self.assignment_grade
        }


    def get_all_assignments():
        return [Course.json(assignment) for assignment in Assignment.query.all()]

    def __repr__(self):
        Assignment_object = {
                 'id': self.id,
                'assignment_name': self.assignment_name,
                'assignment_startdate': dump_datetime(self.assignment_startdate),
                'assignment_duedate': dump_datetime(self.assignment_duedate),
                'assignment_grade': self.assignment_grade
        }
        return json.dumps(Assignment_object)

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(username=user_id).first()


@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login_page.html", error=False)

    user = load_user(request.form["username"])
    if user is None:
        return render_template("login_page.html", error=True)

    if not user.check_password(request.form["password"]):
        return render_template("login_page.html", error=True)

    login_user(user)
    return redirect(url_for('documentation'))



@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))



@app.route('/', methods=["GET","POST"])
def index():
    if request.method == "GET":
        return render_template("main_page.html", timestamp=datetime.now(),title = 'Student Details')

    if not current_user.is_authenticated:
        return render_template("login_page.html", error=True)

    return redirect(url_for('index'))


@app.route('/instructor', methods=["GET","POST"])
def instructor():
    if request.method == "GET":
        return render_template("instructor.html", timestamp=datetime.now(), title = 'Instructor Details')

    if not current_user.is_authenticated:
        return render_template("login_page.html", error=True)

    return redirect(url_for('instructor'))


@app.route('/course', methods=["GET","POST"])
def course():
    if request.method == "GET":
        return render_template("course.html", timestamp=datetime.now(), title = 'Course Details')

    if not current_user.is_authenticated:
        return render_template("login_page.html", error=True)

    return redirect(url_for('course'))


@app.route('/assignment', methods=["GET","POST"])
def assignment():
    if request.method == "GET":
        course_id = request.args.get('Courseid')
        coursedata = Course.query.filter_by(course_id = course_id).first()
        data = db.session.query(Course.id, Course.course_name, Assignment.id, Assignment.assignment_name, Assignment.assignment_grade, Assignment.assignment_startdate, Assignment.assignment_duedate).join(Course,Course.id == Assignment.courses).filter(Course.course_id == course_id).order_by(Course.id).all()
        return render_template("assignment.html", timestamp=datetime.now(), title = 'Assignment Details', course_id = course_id, AssignmentDetails = data, course_name = coursedata)

    if not current_user.is_authenticated:
        return render_template("login_page.html", error=True)

    return redirect(url_for('assignment'))


@app.route('/documentation', methods=["GET","POST"])
def documentation():
    if request.method == "GET":
        return render_template("documentation.html", timestamp=datetime.now(), title = 'Documentation Details')

    if not current_user.is_authenticated:
        return render_template("login_page.html", error=True)

    return redirect(url_for('documentation'))


@app.route('/api/instructor', methods=['GET'])
def get_all_instructor():
    recordcount =  Instructor.query.count();
    return jsonify({'instructor': Instructor.get_all_instructors(), 'record':recordcount})


@app.route('/api/course', methods=['GET'])
def get_all_course():
    recordcount =  Course.query.count();
    return jsonify({'course': db.session.query(Course.course_id, Course.course_name, Course.course_description, Course.course_schedule, Course.course_startdate, Course.course_enddate, Instructor.id, Instructor.first_name, Instructor.last_name, Instructor.title).join(Instructor,Course.instructor_id == Instructor.id).order_by(Course.course_id).all(), 'record':recordcount})


@app.route('/api/assignment', methods=['GET'])
def get_all_assignment():
    recordcount =  Assignment.query.count();
    return jsonify({'assignment': db.session.query(Course.id, Course.course_name, Assignment.id, Assignment.assignment_name, Assignment.assignment_grade, Assignment.assignment_startdate, Assignment.assignment_duedate).join(Course,Course.id == Assignment.courses).order_by(Course.id).all(), 'record':recordcount})


@app.route('/api/assignment/<int:course_id>', methods=['GET'])
def get_all_assignment_id(course_id):
    recordcount =  Assignment.query.count();
    return jsonify({'assignment': db.session.query(Course.id, Course.course_name, Assignment.id, Assignment.assignment_name, Assignment.assignment_grade, Assignment.assignment_startdate, Assignment.assignment_duedate).join(Course,Course.id == Assignment.courses).filter(Course.id == course_id).order_by(Course.id).all(), 'record':recordcount})






