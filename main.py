from flask import Flask, render_template,request,redirect,g
import pymysql,pymysql.cursors
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import flask_login

app = Flask(__name__)

auth = HTTPBasicAuth()
app.secret_key = "cdserfawgtvKL"

def connect_db():
    return pymysql.connect(
        host="10.100.33.60",
        user="nvasiuta",
        password="244805859",
        database="nvasiuta_gulagmedia",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )

def get_db():
    '''Opens a new database connection per request.'''        
    if not hasattr(g, 'db'):
        g.db = connect_db()
    return g.db    

@app.teardown_appcontext
def close_db(error):
    '''Closes the database connection at the end of request.'''    
    if hasattr(g, 'db'):
        g.db.close() 



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
      cursor = get_db().cursor()
      cursor.execute(f"SELECT * FROM `users` WHERE `id`='{user_id}' ")
      result=cursor.fetchone()
      cursor.close()
      get_db().commit()
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


        cursor = get_db().cursor()
        cursor.execute(f"INSERT INTO `users` (`user_name`,`pasword`,`email`,`birthday`) VALUES ('{name}', '{password}', '{emil}','{dob}')")
        cursor.close()
        get_db().commit()






    return render_template("signup.html.jinja")
    

@app.route('/signin/',methods=["GET","POST"])
def signin():
    if request.method == 'POST':
        password = request.form["password"]
        name = request.form["namee"]
        cursor = get_db().cursor()
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
     if flask_login.current_user.is_authenticated==False:
      return render_template("/")
     cursor = get_db().cursor()
     cursor.execute("SELECT * FROM `posts` ORDER BY `posts`.`description` DESC")
     get_db().commit()
     cursor.close()
     post_thing=cursor.fetchall()
     return render_template("feed.html.jinja",posts=post_thing)


@app.route('/post',methods=["POST"])
@flask_login.login_required
def create_post():
     description=request.form["DESCRIPTION"]
     description=request.form["user_id"]


#cursor.execute("INSERT INTO `posts` (`description`, `user_id`)")
