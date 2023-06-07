# write all your SQL queries in this file.
from datetime import datetime
from kursus import conn, login_manager
from flask_login import UserMixin
from psycopg2 import sql

@login_manager.user_loader
def load_user(email):
    cur = conn.cursor()

    user_sql = sql.SQL("""
    SELECT * FROM "user"
    WHERE email = %s
    """)

    cur.execute(user_sql, (email,))
    if cur.rowcount > 0:
        return User(cur.fetchone())
    else:
        return None

class User(tuple, UserMixin):
    def __init__(self, user_data):
        self.email = user_data[0]
        self.password = user_data[1]

    def get_id(self):
       return (self.email)

class Review(tuple): 
    def __init__(self, review_data):
        self.author_id = review_data[0]
        self.course_id = review_data[1]
        self.year = review_data[2]
        self.title = review_data[3]
        self.text = review_data[4]
        self.no_of_upvotes = review_data[5]
        self.no_of_downvotes = review_data[6]
        self.date = review_data[7]
        self.helpfulness = review_data[8]
        self.easiness = review_data[9]
        self.clarity = review_data[10]
        self.workload = review_data[11]
        self.avg_rating = review_data[12]
    
class Course(tuple, UserMixin):
    def __init__(self, course_data):
        self.course_id = course_data[0]
        self.year = course_data[1]
        self.name = course_data[2]
    
    def get_id(self):
        return self.course_id
    
    def get_name(self):
        return self.name 
class Customers(tuple, UserMixin):
    def __init__(self, user_data):
        self.CPR_number = user_data[0]
        self.risktype = False
        self.password = user_data[2]
        self.name = user_data[3]
        self.address = user_data[4]
        self.role = "customer"

    def get_id(self):
       return (self.CPR_number)

class Employees(tuple, UserMixin):
    def __init__(self, employee_data):
        self.id = employee_data[0]
        self.name = employee_data[1]
        self.password = employee_data[2]
        self.role = "employee"

    def get_id(self):
       return (self.id)

class CheckingAccount(tuple):
    def __init__(self, user_data):
        self.id = user_data[0]
        self.create_date = user_data[1]
        self.CPR_number = user_data[2]
        self.amount = 0

class InvestmentAccount(tuple):
    def __init__(self, user_data):
        self.id = user_data[0]
        self.start_date = user_data[1]
        self.maturity_date = user_data[2]
        self.amount = 0

class Transfers(tuple):
    def __init__(self, user_data):
        self.id = user_data[0]
        self.amount = user_data[1]
        self.transfer_date = user_data[2]
        
class Student(tuple,UserMixin):
    def __init__(self, student_data):
        self.id = student_data[0]
        self.name = student_data[1]
        self.field = student_data[2]
        self.level = student_data[3]
        self.no_of_reviews  = student_data[4]    
        self.email= student_data[5]

    def get_id(self):
       return (self.id)

    def get_name(self):
        return (self.name)


def get_distinct_courses():
    cur = conn.cursor()
    sql = """
    SELECT distinct "title english"
    FROM course
    ORDER BY "title english"
    """
    cur.execute(sql)
    tuple_resultset = cur.fetchall()
    cur.close()
    return tuple_resultset

def get_reviewed_courses():
    cur = conn.cursor()
    sql = """
    SELECT distinct "title english"
    FROM course as c
    INNER JOIN review as r on c.course_id = r.course_id and c.year = r.year
    ORDER BY "title english"
    """
    cur.execute(sql)
    tuple_resultset = cur.fetchall()
    cur.close()
    return tuple_resultset

def get_Course(name, year):
    cur = conn.cursor()
    sql = """
    SELECT course_id, year, "title english" FROM COURSE
    WHERE  "title english" = %s AND year = %s 
    """
    cur.execute(sql, (name, year))
    course = Course(cur.fetchone()) if cur.rowcount > 0 else None;
    return course

def get_Course_id(name):
    cur = conn.cursor()
    sql = f"SELECT DISTINCT course_id FROM COURSE WHERE" + """ "title english" """ +  f"= '{name}'"
    cur.execute(sql, (name))
    course_id = cur.fetchone() if cur.rowcount > 0 else None;
    return course_id

def obtain_avg(param, c_id):
    cur = conn.cursor()
    sql = f"SELECT AVG({param}) FROM review WHERE course_id = '{c_id}'"
    cur.execute(sql)
    avg_scores = cur.fetchone() if cur.rowcount > 0 else None;
    return avg_scores

def insert_Review(author_id, course_id, year, title, text, date, helpfulness, easiness, clarity, workload, avg_rating):
    cur = conn.cursor()
    sql = """
    INSERT INTO review (author_id, course_id, "year", title, text, no_of_upvotes, no_of_downvotes, 
                        "date", helpfulness, easiness, clarity, workload, avg_rating)
    values (%s, %s, %s, %s, %s, 0, 0, %s, %s, %s, %s, %s, %s);
    """
    cur.execute(sql, (author_id, course_id, year, title, text, 
                        date, helpfulness, easiness, clarity, workload, avg_rating))
    conn.commit()
    cur.close()

def get_reviews(course_id):
    cur = conn.cursor()
    sql = f"SELECT * FROM review WHERE course_id = '{course_id}'"
    cur.execute(sql)
    reviews = cur.fetchall() if cur.rowcount > 0 else None
    cur.close()
    return reviews

def insert_User(email, password):
    cur = conn.cursor()
    sql = """
    INSERT INTO "user"
    VALUES (%s, %s)
    """
    cur.execute(sql, (email, password))
    # Husk commit() for INSERT og UPDATE, men ikke til SELECT!
    conn.commit()
    cur.close()

def insert_Student(name, field, level, email):
    cur = conn.cursor()
    # print(name, field, level, email)
    sql = """
    INSERT INTO student (name, studies, bsc_msc, no_of_reviews, email)
    VALUES (%s, %s,%s,0,%s)
    """
    cur.execute(sql, (name,field,level,email))
    # Husk commit() for INSERT og UPDATE, men ikke til SELECT!
    conn.commit()
    cur.close()


def select_Student(email):
    cur = conn.cursor()
    sql = """
    SELECT * FROM student
    WHERE email=%s
    """
    cur.execute(sql, (email,))
    student = Student(cur.fetchone()) if cur.rowcount > 0 else None;
    cur.close()
    return student

def select_User(email):
    cur = conn.cursor()
    sql = """
    SELECT * FROM "user"
    WHERE email = %s
    """
    cur.execute(sql, (email,))
    user = User(cur.fetchone()) if cur.rowcount > 0 else None;
    cur.close()
    return user