from django.shortcuts import render
from multiprocessing import context
from flask import render_template, url_for, flash, redirect, request, Blueprint
from kursus import app, conn, bcrypt
from kursus.forms import UserLoginForm, RegisterForm, SelectCourseForm
from flask_login import login_user, current_user, logout_user, login_required
from kursus.models import get_distinct_courses, get_reviewed_courses, select_Student, select_User, User, insert_User, insert_Student, get_Course, get_Course_id, get_reviews
from kursus.models import obtain_avg, get_personal_reviews, get_Course_names

from kursus import roles, mysession

Login = Blueprint('Login', __name__)
bp = Blueprint('auth', __name__, url_prefix='/auth')


posts = [{}]

@Login.route('/profile', methods=('GET', 'POST'))
@login_required
def profile():
    student = select_Student(current_user.email)
    reviews = get_personal_reviews(student.get_id())
    with_course_names = get_Course_names(student.get_id())
   # print(with_course_names)
    return render_template('profile.html', name=student.get_name(), reviews=reviews, course_names = with_course_names)

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
    student = None
    if current_user.is_authenticated:
        student = select_Student(current_user.email)
    mysession["state"]="home or /"


    dis_courses = get_reviewed_courses()
    courses = map(lambda course: course[0], dis_courses)
    
    return render_template('home.html', courses = courses, name = student.get_name() if student != None else None)


@Login.route("/about")
def about():
    student = select_Student(current_user.email)
    #202212
    mysession["state"]="about"
    # print(mysession)
    return render_template('about.html', title='About',  name=student.get_name())


@Login.route("/login", methods=['GET', 'POST'])
def login():

    #202212
    mysession["state"]="login"
   # print(mysession)
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
            #print(mysession)


            login_user(user, remember=form.remember.data)
            flash('Login successful.','success')
            return redirect(url_for('Login.profile'))
        else:
            flash('Login Unsuccessful. Please check identifier and password', 'danger')

    return render_template('login.html', title='Login', form=form
    )


@Login.route("/logout")
def logout():
    #202212
    mysession["state"]="logout"
   # print(mysession)

    logout_user()
    return redirect(url_for('Login.home'))


@Login.route('/course', methods=['GET', 'POST'])
def course_page():
    student = select_Student(current_user.email)
    if request.method == 'POST':
        form = SelectCourseForm()
        course_id = get_Course_id(form.course.data)
        if course_id == None: 
            flash('Please select a course dummy', 'danger')
            return redirect(url_for('Login.home'))

        reviews = get_reviews(course_id[0])
        avgScores= [obtain_avg('clarity', course_id[0]),obtain_avg('easiness', course_id[0]),obtain_avg('workload', course_id[0]), obtain_avg('helpfulness', course_id[0]), obtain_avg('avg_rating', course_id[0])]
        return render_template('review.html', title=form.course.data, code=course_id[0], reviews=reviews, avgScores=avgScores, name = student.get_name())
    
    return render_template('review.html')