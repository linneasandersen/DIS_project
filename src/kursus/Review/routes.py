# from os import remove
# from flask import render_template, url_for, flash, redirect, request, Blueprint
# from kursus import app, conn, bcrypt
# from kursus.forms import WriteReviewForm, SelectCourseForm
# from flask_login import login_user, current_user, logout_user, login_required
# from kursus.models import Review, get_Course, get_Course_id, get_reviews, select_Student, User, get_distinct_courses, insert_Review
# from kursus.models import select_cus_accounts
# #202212
# from kursus import roles, mysession

# import sys, datetime

# #202212
# # roles is defined in the init-file
# from kursus import roles, mysession

# # iEmployee = 1
# # iCustomer = 2

# Review = Blueprint('Review', __name__)


# @Review.route('/course', methods=['GET', 'POST'])
# def course_page():
#     if request.method == 'POST':
#         form = SelectCourseForm()
#         course_id = get_Course_id(form.course.data)
#         reviews = get_reviews(course_id)
#         print(reviews)
#         return redirect(url_for('Login.profile'))
#     return render_template('review.html', title = form.course.data, code = course_id)