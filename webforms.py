from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import (
    BooleanField,
    PasswordField,
    StringField,
    SubmitField,
    TextAreaField,
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
    # content = StringField("Content", validators=[DataRequired()], widget=TextArea())
    content = CKEditorField("Body", validators=[DataRequired()])
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
    about_author = TextAreaField("About Author")
    password_hash = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            EqualTo("password_hash2", message="Passwords Must Match"),
        ],
    )
    password_hash2 = PasswordField("Confirm Password", validators=[DataRequired()])
    profile_pic = FileField("Profile Pic")

    submit = SubmitField("Submit")  # submit button


class PasswordForm(FlaskForm):
    # if form is submitted without any data, it will show an error message
    email = StringField("What is your email?", validators=[DataRequired()])
    password_hash = PasswordField("What is your password?", validators=[DataRequired()])

    submit = SubmitField("Submit")  # submit button


class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()])
    submit = SubmitField("Submit")


# create a form class
class NamerForm(FlaskForm):
    name = StringField(
        "What is your name?", validators=[DataRequired()]
    )  # if form is submitted without any data, it will show an error message
    submit = SubmitField("Submit")  # submit button
