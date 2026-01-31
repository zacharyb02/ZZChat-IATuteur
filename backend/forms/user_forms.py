from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[
        DataRequired(),
        Length(min=3, max=80)
    ])

    email = StringField("Email", validators=[
        DataRequired(),
        Email()
    ])

    password_hash = PasswordField("Password", validators=[
        DataRequired(),
        Length(min=6)
    ])

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[
        DataRequired(),
        Email()
    ])

    password_hash = PasswordField("Password", validators=[
        DataRequired(),
        Length(min=6)
    ])

