from flask import Flask
import psycopg2
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = 'fc089b9218301ad987914c53481bff04'

# set your own database here
db = "dbname='postgres' user='superbruger' host='127.0.0.1' password = 'dis'"
conn = psycopg2.connect(db)

bcrypt = Bcrypt(app)


login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

roles = ["ingen","employee","customer"]

mysession = {"state" : "initializing","role" : "Not assigned", "id": 0 ,"age" : 202212}


from kursus.Login.routes import Login
from kursus.User.routes import User

app.register_blueprint(Login)
app.register_blueprint(User)