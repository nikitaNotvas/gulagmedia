from flask import Flask, render_template,request,redirect
import pymysql,pymysql.cursors
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
#@auth.login_required



conn = pymysql.connect(
    database="nvasiuta_gulagmedia",
    user="nvasiuta",
    password="244805859",
    host='10.100.33.60',
    cursorclass=pymysql.cursors.DictCursor
)


auth = HTTPBasicAuth()
app = Flask(__name__)

users = {
    "humano": generate_password_hash ("no")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username


@app.route('/',methods=["GET","POST"])
def index():
    return render_template("home.html.jinja")


@app.route('/signup/',methods=["GET","POST"])
def signup():
    return render_template("signup.html.jinja")
    

@app.route('/signin/',methods=["GET","POST"])
def signin():
    return render_template("signin.html.jinja")


