from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError

class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=50)])
    email = StringField('E-mail', validators=[DataRequired(), Length(min=1, max=20)], render_kw={"placeholder": "Please use your KU-email"})
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=255)])
    field = StringField('Field of Study', validators=[DataRequired(), Length(min=1, max=50)])
    level = SelectField('Level', choices=[], validators=[DataRequired()])
    submit = SubmitField('Register')

class UserLoginForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class WriteReviewForm(FlaskForm):
    year = SelectField('Year', choices=[], validators=[DataRequired()])
    course = StringField('Course', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=100)])
    text = StringField('Text', validators=[DataRequired()])
    helpfulness = SelectField('Helfulness', choices=[], validators=[DataRequired()])
    easiness = SelectField('Easiness', choices=[], validators=[DataRequired()] )
    clarity = SelectField('Clarity', choices=[], validators=[DataRequired()])
    workload = SelectField('Workload', choices=[], validators=[DataRequired()])





class TransferForm(FlaskForm):
    amount = IntegerField('amount', 
                        validators=[DataRequired()])
    #sourceAccountTest = SelectField('From Account test:', choices=dropdown_choices, validators=[DataRequired()])
    sourceAccount = SelectField('From Account:'  , choices=[], coerce = int, validators=[DataRequired()])
    targetAccount = SelectField('Target Account:', choices=[], coerce = int, validators=[DataRequired()])
    submit = SubmitField('Confirm')

class DepositForm(FlaskForm):
    amount = IntegerField('amount', 
                       validators=[DataRequired()])
    submit = SubmitField('Confirm')
    
class InvestForm(FlaskForm):
    submit = SubmitField('Confirm')