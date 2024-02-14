from flask import Flask, render_template,request,redirect
import pymysql,pymysql.cursors
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import flask_login


conn = pymysql.connect(
    database="nvasiuta_gulagmedia",
    user="nvasiuta",
    password="244805859",
    host='10.100.33.60',
    cursorclass=pymysql.cursors.DictCursor
)


auth = HTTPBasicAuth()
app = Flask(__name__)
app.secret_key = "cdserfawgtvKL"

login_manager = flask_login.LoginManager()

login_manager.init_app(app)
class User:
    is_active=True
    is_authenticated=True
    is_anonymous=False
    def __init__(self,id,user_name):
        self.id=id
        self.user_name=user_name
    def get_id(self):
         return str(self.id)

@login_manager.user_loader
def load_user(user_id):
      cursor = conn.cursor()
      cursor.execute(f"SELECT * FROM `users` WHERE `id`='{user_id}' ")
      result=cursor.fetchone()
      cursor.close()
      conn.commit()
      if result is None:
           return None
      return User(result["id"],result["user_name"])


@app.route('/',methods=["GET","POST"])
def index():
    if flask_login.current_user.is_authenticated:
         return redirect('/feed')
    return render_template("home.html.jinja")


@app.route('/signup/',methods=["GET","POST"])
def signup():
    if request.method == 'POST':
        name = request.form["name"]
        password = request.form["password"]
        emil = request.form["emil"]
        dob = request.form["dateofbirth"]


        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO `users` (`user_name`,`pasword`,`email`,`birthday`) VALUES ('{name}', '{password}', '{emil}','{dob}')")
        cursor.close()
        conn.commit()






    return render_template("signup.html.jinja")
    

@app.route('/signin/',methods=["GET","POST"])
def signin():
    if request.method == 'POST':
        password = request.form["password"]
        name = request.form["namee"]
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM `users` WHERE `user_name` = '{name}'")
        thing=cursor.fetchone()
        if password == thing['pasword']:
                user = load_user(thing["id"])
                flask_login.login_user(user)
                return redirect('/feed')
    return render_template("signin.html.jinja")


@app.route('/feed')
@flask_login.login_required
def post_feed():
     if flask_login.current_user.is_authenticated==True:
      return render_template("feed.html.jinja")
     cursor = conn.cursor()
     cursor.execute("SELECT * FROM `posts` ORDER BY `time and date`")
     cursor.close()
     conn.commit()
     post_thing=cursor.fetchall()
     return render_template("feed.html.jinja",posts=post_thing)