from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    PasswordField,
    StringField,
    SubmitField,
    ValidationError,
    validators,
)
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea


# create login form
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


# create a posts form
class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = StringField("Content", validators=[DataRequired()], widget=TextArea())
    author = StringField("Author")
    slug = StringField("Slug", validators=[DataRequired()])
    submit = SubmitField("Submit")


# vid 8: create a form class
class UserForm(FlaskForm):
    # if form is submitted without any data, it will show an error message
    name = StringField("Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    favorite_color = StringField("Favorite Color")
    password_hash = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            EqualTo("password_hash2", message="Passwords Must Match"),
        ],
    )
    password_hash2 = PasswordField("Confirm Password", validators=[DataRequired()])

    submit = SubmitField("Submit")  # submit button


class PasswordForm(FlaskForm):
    # if form is submitted without any data, it will show an error message
    email = StringField("What is your email?", validators=[DataRequired()])
    password_hash = PasswordField("What is your password?", validators=[DataRequired()])

    submit = SubmitField("Submit")  # submit button


# create a form class
class NamerForm(FlaskForm):
    name = StringField(
        "What is your name?", validators=[DataRequired()]
    )  # if form is submitted without any data, it will show an error message
    submit = SubmitField("Submit")  # submit button
