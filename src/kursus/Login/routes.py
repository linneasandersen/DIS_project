from flask import render_template, url_for, flash, redirect, request, Blueprint
from kursus import app, conn, bcrypt
from kursus.forms import UserLoginForm, RegisterForm
from flask_login import login_user, current_user, logout_user, login_required
from kursus.models import select_User, User, insert_User
from kursus.models import select_cus_accounts
#202212
from kursus import roles, mysession

Login = Blueprint('Login', __name__)
bp = Blueprint('auth', __name__, url_prefix='/auth')


posts = [{}]

@Login.route('/register', methods=('GET', 'POST'))
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        
        user = User([form.email.data, form.password.data])

        # Derefter tjek om hashet af adgangskoden passer med det fra databasen...
        # Her checkes om der er logget på
        # if user != None and bcrypt.check_password_hash(user[1], form.password.data):
        if user != None:
            mysession["email"] = form.email.data
            mysession["password"] = form.password.data
            print(mysession)
            insert_User(form.email.data,form.password.data)
            flash('register  successful.','success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('Login.home'))
        else:
            flash('Login Unsuccessful. Please check identifier and password', 'danger')
    return render_template('login.html', title='Login', form=form
    )
    
   


@Login.route("/")
@Login.route("/home")
def home():
    #202212
    mysession["state"]="home or /"
    print(mysession)
    #202212
    role =  mysession["role"]
    print('role: '+ role)

    return render_template('home.html', posts=posts, role=role)


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
    if form.validate_on_submit():

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
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('Login.home'))
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
#teachers={{"id": str(1234), "name":"anders"},}
#data={"user_id": str(user_id), "total_trials":total_trials}

    #hvor gemmes login-bruger-id?

@Login.route("/logout")
def logout():
    #202212
    mysession["state"]="logout"
    print(mysession)

    logout_user()
    return redirect(url_for('Login.home'))


# @Login.route("/account")
# @login_required
# def account():
#     mysession["state"]="account"
#     print(mysession)
#     # role =  mysession["role"]
#     # print('role: '+ role)

#     accounts = select_cus_accounts(current_user.get_id())
#     print(accounts)
#     return render_template('account.html', title='Account'
#     , acc=accounts, role=role
#     )
