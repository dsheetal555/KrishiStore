from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired,Email,EqualTo,length
from myproject.models import User
from wtforms import ValidationError

class LoginForm(FlaskForm):
    email = StringField(validators=[DataRequired(),Email(message=('Not a valid email address'))])
    password = PasswordField(validators=[DataRequired(),length(min=8)])
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    fullname = StringField(validators=[DataRequired()])
    email = StringField(validators=[DataRequired(),Email(message=('Not a valid email address'))])
    phone_no = StringField(validators=[DataRequired(),length(max=10)])
    pwd = PasswordField(validators=[DataRequired(),EqualTo('conf_pwd', message='Passwords must match'),length(min=8)])
    conf_pwd = PasswordField(validators=[DataRequired(),length(min=8)])
    country = SelectField('Select Country',choices = [('India', 'India'), ('USA', 'USA'),('UK', 'UK')],validators=[DataRequired()])
    submit = SubmitField('SignUp')

    def check_email(self, field):
        # Check if not None for that user email!
        if User.query.filter_by(email=field.data).first():
            return ('Your email has been registered already!')

class Quantity(FlaskForm):
    quantity = IntegerField(validators=[DataRequired()])
