from flask import Flask, render_template,request,redirect
import pymysql,pymysql.cursors
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash



conn = pymysql.connect(
    database="nvasiuta_todos",
    user="nvasiuta",
    password="244805859",
    host='10.100.33.60',
    cursorclass=pymysql.cursors.DictCursor
)


auth = HTTPBasicAuth()
app = Flask(__name__)


@app.route('/',methods=["GET","POST"])
@auth.login_required
def index():
