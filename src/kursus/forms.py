from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError

class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    field = StringField('Field of Study', validators=[DataRequired()])
    level = SelectField('Level', choices=[],validators=[DataRequired()])
    submit = SubmitField('Register')


class UserLoginForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')



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