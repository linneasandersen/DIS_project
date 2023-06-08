# KU Course Reviewer

This project enables people to see KU courses and how they are reviewed by students. Students can review courses and see how a certain course is rated before choosing to enroll in the course.

## Initialize the database

1. Make sure you have a superuser called 'superbruger' with password 'dis'
2. Make sure you have a database called 'postgres'
3. Find your way to ../DIS_PROJECT/src/kursus
4. Run:

> $ psql -U superbruger -d postgres -f schema.sql

Alternatively, you can set the database in src/__init__.py in line 10 and then run:

> $ psql -U your_user_name -d your_db_name -f schema.sql

## Initialize virtual environment

Run the following from ../DIS_PROJECT/

> $ bash init.sh

## Run the website

Run

> $ cd src

> $ . .venv/bin/activate

> $ export FLASK_APP=run.py

> $ flask run

Should the above not work, follow these commands step-by-step:

## Virtual environment

Create a virtual environment

> $ python3 -m venv .venv

Activate the virtual environment

> $ . .venv/bin/activate

Run the code below to install the necessary modules.

> $ pip install -r requirements.txt

## Running the website

Run the following commands:

> $ export FLASK_APP=run.py

> $ flask run

For Windows you may have to use the SET command instead of EXPORT. Ex set FLASK_APP=run.py; flask run. Also remember to add the path to your postgres bin-directory in order to run (SQL interpreter) and other postgres programs in any shell.

## Navigating the website

1. Open a browser and go to 127.0.0.1:5000. We recommend Chrome.
2. On the front page, you can choose a course for which to see reviews
3. To create a review, you must be logged in. Use the register form or log in using the following email: admin@alumni.ku.dk and password: qwerty
4. You can now create a review and see your own reviews

## Further improvements and known bugs

We have a lot of ideas regarding how to further improve the website:

* Validation of KU-emails. To ensure only KU students can write reviews, it would be necessary to validate the KU-emails. Currently, we only limit the amount of characters in a user's email to 20 characters.
* Improved security. Currently, there are no requirements for choosing a password other than they should be no longer than 255 characters. To increase security, it would be good to have requirements for the password (such as a number and a special character) and we could also use hashing.
* Approving reviews. In order to avoid harmful language, it would be a good idea to approve each review before it is posted.
* Adding more roles. We would need to have admin users to e.g. be able to approve reviews.
* When selecting a course on the 'write a review'-page and on the front page, we would like to have a searchable drop down menu, since there are a lot of courses.
* Upvotes and downvotes for reviews.
* Incrementing the no_of_reviews attribute in the student table

We are also aware of a bug:

* On the 'write a review'-page when the user is prompted to choose which course to review, we select distinct course names, meaning that if two different courses have the same English title, they are displayed only as one. This causes some problems, but the scope is small.

## E/R diagram

As specified in our E/R diagram, we have omitted the full list of attributes for the course table since it is very long. In full, the course table contains the following attributes:

* course_id
* description language
* language of instruction
* title danish
* title english
* cancelled, level
* board of studies
* responsible institute
* participating institute
* names of course responsible
* emails of course responsible
* lecturers danish
* lecturers english
* length
* temporal placement
* schedule group
* method of teaching danish
* method of teaching english
* formal requirements danish
* formal requirements english
* academic prerequisites danish
* academic prerequisites english
* course notes danish
* course notes english
* ECTS of exam
* exam requirements for registration danish
* exam requirements for registration english
* test form of exam
* length of exam danish
* length of exam english
* exam aids
* faculty
* year
