from os import remove
from flask import render_template, url_for, flash, redirect, request, Blueprint
from kursus import app, conn, bcrypt
from kursus.forms import WriteReviewForm
from flask_login import login_user, current_user, logout_user, login_required
from kursus.models import Review, get_Course, select_Student, User, get_distinct_courses, insert_Review
from kursus.models import select_cus_accounts
#202212
from kursus import roles, mysession

import sys, datetime

#202212
# roles is defined in the init-file
from kursus import roles, mysession

# iEmployee = 1
# iCustomer = 2

User = Blueprint('User', __name__)

    
def calcAvgScore (form : WriteReviewForm):
     return (int(form.clarity.data) + int(form.easiness.data) + int(form.helpfulness.data) + int(form.workload.data)) / 4

@User.route("/write", methods=['GET', 'POST'])
def write():
    form = WriteReviewForm()
    if request.method == 'POST':
        
        email = current_user.get_id()
        student = select_Student(email)
        course = get_Course(form.course.data, form.year.data)
        if course == None: 
            flash('Course was not held this year', 'danger')
            return redirect(url_for('User.write'))
        r = Review([student.get_id(), course.get_id(), form.year.data, form.title.data,
                    form.text.data, 0, 0, datetime.date.today(), form.helpfulness.data, form.easiness.data,
                    form.clarity.data, form.workload.data, calcAvgScore(form)])

        if r != None:
            print("valid review")
            insert_Review(r.author_id, r.course_id, r.year, r.title, r.text, r.date, r.helpfulness,
                            r.easiness, r.clarity, r.workload, r.avg_rating)
            flash('Review submitted.','success')
            return redirect(url_for('Login.home'))
        else:
            flash('Login Unsuccessful. Please check identifier and password', 'danger')



    courses = get_distinct_courses()
    courses = map(lambda course: course[0], courses)

    return render_template('write.html', courses=courses)
"""

@Customer.route("/transfer", methods=['GET', 'POST'])
def transfer():
    if not current_user.is_authenticated:
        flash('Please Login.','danger')
        return redirect(url_for('Login.login'))

    # CUS7 is the customer transfer. Create new endpoint.
    # EUS10 is the employee transfer.
    # manageCustor/ er EUS!=
    # transfer/  må være CUS7
    # move to customer DONE
    # duplicate back and change database access here


    if not mysession["role"] == roles[iCustomer]:
        flash('transfer money customer mode.','danger')
        return redirect(url_for('Login.login'))


    CPR_number = current_user.get_id()
    print(CPR_number)
    dropdown_accounts = select_cus_accounts(current_user.get_id())
    drp_accounts = []
    for drp in dropdown_accounts:
        drp_accounts.append((drp[3], drp[1]+' '+str(drp[3])))
    print(drp_accounts)
    form = TransferForm()
    form.sourceAccount.choices = drp_accounts
    form.targetAccount.choices = drp_accounts
    if form.validate_on_submit():
        date = datetime.date.today()
        amount = form.amount.data
        from_account = form.sourceAccount.data
        to_account = form.targetAccount.data
        transfer_account(date, amount, from_account, to_account)
        flash('Transfer succeed!', 'success')
        return redirect(url_for('Login.home'))
    return render_template('transfer.html', title='Transfer', drop_cus_acc=dropdown_accounts, form=form)



@Customer.route("/invest", methods=['GET', 'POST'])
def invest():

    #202212
    # Her laves et login check
    if not current_user.is_authenticated:
        flash('Please Login.','danger')
        return redirect(url_for('Login.login'))

    #202212
    #customer
    # CUS4; CUS4-1, CUS4-4
    # TODO-CUS There us no customer counterpart
    if not mysession["role"] == roles[iCustomer]:
        flash('Viewing investents is customer only.','danger')
        return redirect(url_for('Login.login'))


    mysession["state"]="invest"
    print(mysession)

    #202212
    # i think this view works for employee and customer but the
    # view is different as employees have customers.
    # CUS4; CUS4-1, CUS4-4
    print(current_user.get_id())

    investments = select_cus_investments(current_user.get_id())
    investment_certificates = select_cus_investments_with_certificates(current_user.get_id())
    investment_sums = select_cus_investments_certificates_sum(current_user.get_id())
    return render_template('invest.html', title='Investments', inv=investments
    , inv_cd_list=investment_certificates
    , inv_sums=investment_sums)


@Customer.route("/deposit", methods=['GET', 'POST'])
def deposit():
    if not current_user.is_authenticated:
        flash('Please Login.','danger')
        return redirect(url_for('Login.login'))


    #202212
    #EUS-CUS10
    # move to employee object
    if not mysession["role"] == roles[iEmployee]:
        flash('Deposit is employee only.','danger')
        return redirect(url_for('Login.login'))

    mysession["state"]="deposit"
    print(mysession)


    form = DepositForm()
    if form.validate_on_submit():
        amount=form.amount.data
        CPR_number = form.CPR_number.data
        update_CheckingAccount(amount, CPR_number)
        flash('Succeed!', 'success')
        return redirect(url_for('Login.home'))
    return render_template('deposit.html', title='Deposit', form=form)

@Customer.route("/summary", methods=['GET', 'POST'])
def summary():
    if not current_user.is_authenticated:
        flash('Please Login.','danger')
        return redirect(url_for('Login.login'))
    if form.validate_on_submit():
        pass
        flash('Succeed!', 'success')
        return redirect(url_for('Login.home'))
    return render_template('deposit.html', title='Deposit', form=form)
"""