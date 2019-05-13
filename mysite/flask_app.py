# A very simple Flask Hello World app for you to get started with...
from datetime import datetime
from flask import Flask, redirect, render_template, request, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import login_user, LoginManager, UserMixin, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
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

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))

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
    instructor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    Instructor_key = db.relationship('User', foreign_keys=instructor_id)

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
                'instructor_id': self.instructor_id
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
                'instructor_id': self.instructor_id
        }
        return json.dumps(instructor_object)


class Course(db.Model):
    __tablename__ = "sgb_Course"

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.String(150))
    course_name = db.Column(db.String(150))
    course_description = db.Column(db.String(4000))
    course_schedule = db.Column(db.String(200))
    course_startdate = db.Column(db.Date)
    course_enddate = db.Column(db.Date)



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


@app.route('/documentation', methods=["GET","POST"])
def documentation():
    if request.method == "GET":
        return render_template("documentation.html", timestamp=datetime.now(), title = 'Documentation Details')

    if not current_user.is_authenticated:
        return render_template("login_page.html", error=True)

    return redirect(url_for('documentation'))


@app.route('/api/instructor', methods=['GET'])
def get_all_instructor():
    return jsonify({'instructor': Instructor.get_all_instructors()})





