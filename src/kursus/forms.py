from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError

class RegisterForm(FlaskForm):
    email = IntegerField('E-mail', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Register')


class UserLoginForm(FlaskForm):
    email = IntegerField('E-mail', validators=[DataRequired()])
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