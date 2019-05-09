# A very simple Flask Hello World app for you to get started with...
from datetime import datetime
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import login_user, LoginManager, UserMixin, login_required, logout_user, current_user
from werkzeug.security import check_password_hash


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


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(username=user_id).first()

class Comment(db.Model):

    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(4096))
    posted = db.Column(db.DateTime, default=datetime.now)
    commenter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    commenter = db.relationship('User', foreign_keys=commenter_id)

#comments = []


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
    return redirect(url_for('index'))



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
        return redirect(url_for('index'))

    return redirect(url_for('index'))



@app.route('/documentation', methods=["GET","POST"])
def documentation():
    if request.method == "GET":
        return render_template("documentation.html", comments=Comment.query.all(), timestamp=datetime.now(), title = 'Documentation Details')

    if not current_user.is_authenticated:
        return redirect(url_for('documentation'))


    return redirect(url_for('documentation'))