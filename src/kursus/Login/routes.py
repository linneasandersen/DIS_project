from django.shortcuts import render
from multiprocessing import context
from flask import render_template, url_for, flash, redirect, request, Blueprint
from kursus import app, conn, bcrypt
from kursus.forms import UserLoginForm, RegisterForm
from flask_login import login_user, current_user, logout_user, login_required
from kursus.models import get_distinct_courses, get_reviewed_courses, select_Student, select_User, User, insert_User, insert_Student
from kursus.models import select_cus_accounts
#202212
from kursus import roles, mysession

Login = Blueprint('Login', __name__)
bp = Blueprint('auth', __name__, url_prefix='/auth')


posts = [{}]

@Login.route('/profile', methods=('GET', 'POST'))
@login_required
def profile():
    student = select_Student(current_user.email)
    return render_template('profile.html', name=student.get_name()) 

@Login.route('/register', methods=('GET', 'POST'))
def register():
    form = RegisterForm()
    if request.method == 'GET':
        print("res")

    if request.method == 'POST':
        print("res2")
        
        user = User([form.email.data, form.password.data])

        # Derefter tjek om hashet af adgangskoden passer med det fra databasen...
        # Her checkes om der er logget på
        # if user != None and bcrypt.check_password_hash(user[1], form.password.data):
        if user != None:
            print("valid user")
            print(form.field.data)
            mysession["email"] = form.email.data
            mysession["password"] = form.password.data
            print(mysession)
            insert_User(form.email.data,form.password.data)
            insert_Student(form.name.data,form.field.data,form.level.data,form.email.data)
            flash('Register successful.','success')
            return redirect(url_for('Login.login'))
        else:
            flash('Login Unsuccessful. Please check identifier and password', 'danger')

    return render_template('register.html', title='Login', form=form)
    
   
@Login.route('/home', methods=('GET', 'POST'))
@Login.route("/")
@Login.route("/home")
def home():
    #202212
    mysession["state"]="home or /"
    print(mysession)
    #202212
    role =  mysession["role"]
    print('role: '+ role)
    dis_courses = get_reviewed_courses()
    courses = map(lambda course: course[0], dis_courses)

    return render_template('home.html', courses=courses)


@Login.route("/about")
def about():
    #202212
    mysession["state"]="about"
    print(mysession)
    return render_template('about.html', title='About')


@Login.route("/login", methods=['GET', 'POST'])
def login():

    #202212
    mysession["state"]="login"
    print(mysession)
    role=None

    # jeg tror det her betyder at man er er logget på, men har redirected til login
    # så kald formen igen
    # men jeg forstår det ikke
    if current_user.is_authenticated:
        return redirect(url_for('Login.home'))

    form = UserLoginForm()

    # Først bekræft, at inputtet fra formen er gyldigt... (f.eks. ikke tomt)
    if request.method == 'POST':

        #"202212"
        # her checkes noget som skulle være sessionsvariable, men som er en GET-parameter
        # implementeret af AL. Ideen er at teste på om det er et employee login
        # eller om det er et customer login.
        # betinget tildeling. Enten en employee - eller en customer instantieret
        # Skal muligvis laves om. Hvad hvis nu user ikke blir instantieret
        user = select_User(form.email.data)

        # Derefter tjek om hashet af adgangskoden passer med det fra databasen...
        # Her checkes om der er logget på
        # if user != None and bcrypt.check_password_hash(user[1], form.password.data):
        if user != None:
            mysession["email"] = form.email.data
            print(mysession)
            #202212
            ####### print("role:" + user.role)
            # if user.role == 'employee':
            #     mysession["role"] = roles[1] #employee
            # elif user.role == 'customer':
            #     mysession["role"] = roles[2] #customer
            # else:
            #     mysession["role"] = roles[0] #ingen
            #print(roles)

            login_user(user, remember=form.remember.data)
            flash('Login successful.','success')
            return redirect(url_for('Login.profile'))
        else:
            flash('Login Unsuccessful. Please check identifier and password', 'danger')
    #202212
    #Get lists of employees and customers
    # teachers = [{"id": str(6234), "name":"anders. teachers with 6."}, {"id": str(6214), "name":"simon"},
    #             {"id": str(6862), "name":"dmitry"}, {"id": str(6476), "name":"finn"}]
    # parents =  [{"id": str(4234), "name":"parent-anders. parents with 4."}, {"id": str(4214), "name":"parent-simon"},
    #             {"id": str(4862), "name":"parent-dmitry"}, {"id": str(4476), "name":"parent-finn"}]
    # students = [{"id": str(5234), "name":"student-anders. students with 5."}, {"id": str(5214), "name":"student-simon"},
    #             {"id": str(5862), "name":"student-dmitry"}, {"id": str(5476), "name":"student-finn"}]

    #202212
    # role =  mysession["role"]
    # print('role: '+ role)

    #return render_template('login.html', title='Login', is_employee=is_employee, form=form)
    return render_template('login.html', title='Login', form=form
    )


@Login.route("/logout")
def logout():
    #202212
    mysession["state"]="logout"
    print(mysession)

    logout_user()
    return redirect(url_for('Login.home'))


