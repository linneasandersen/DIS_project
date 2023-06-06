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

Review = Blueprint('Review', __name__)


@Review.route('/course', methods=['GET', 'POST'])
def course_page(course_name):
    
    course_data = {
    'title': 'Introduction to Computer Science',
    'code': 'Computer+Systems+(CompSys)',
    'description': 'This course provides an introduction to computer science and programming.',
    # Add more course data as needed
    }

        # Pass the course data to the templat
    return render_template('review.html', course=course_data)