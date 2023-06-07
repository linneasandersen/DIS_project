from os import remove
from flask import render_template, url_for, flash, redirect, request, Blueprint
from kursus import app, conn, bcrypt
from kursus.forms import WriteReviewForm, DeletedReviewForm
from flask_login import login_user, current_user, logout_user, login_required
from kursus.models import Review, get_Course, select_Student, User, get_distinct_courses, insert_Review, delete_review

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
    student = select_Student(current_user.email)
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

    return render_template('write.html', courses=courses, name=student.get_name())

@User.route("/delete-review", methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        form = DeletedReviewForm(request.form)
        review_id = form.review_id.data
        print(review_id)
        delete_review(review_id)
        flash('Review deleted.','success')
        return redirect(url_for('Login.profile'))

    return render_template('about.html')