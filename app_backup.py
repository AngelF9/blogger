from datetime import date, datetime

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash, generate_password_hash
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

# create a flask instance by calling app
app = Flask(__name__)

# vid 9: old sqllite database
# vid 8: add database
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"

# vid 9: new sqllite database
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://root:new_password@localhost/our_users"
)


# configure the secret key
app.config["SECRET_KEY"] = "my super secret key"

# vid 8: initialize the database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Flask_Login stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_veiw = "login"


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


# create login form
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


# create login page
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            # check the hash against password created and password inputed into form
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash("Login successfull")

                return redirect(url_for("dashboard"))
            else:
                flash("Wrong password, try again.")
        else:
            flash("That user doesn't exist, try again")

    return render_template("login.html", form=form)


# create logout page
@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    flash("You have been logged out")
    return redirect(url_for("login"))


# create dashboard page
@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    form = UserForm()
    id = current_user.id
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form["name"]
        name_to_update.email = request.form["email"]
        name_to_update.favorite_color = request.form["favorite_color"]
        name_to_update.username = request.form["username"]
        try:
            db.session.commit()
            flash("User updated successfully!")
            return render_template(
                "dashboard.html", form=form, name_to_update=name_to_update
            )
        except:
            flash("Error! Looks like there was a problem. Try again")
            return render_template(
                "dashboard.html", form=form, name_to_update=name_to_update
            )
    else:
        return render_template(
            "dashboard.html", form=form, name_to_update=name_to_update, id=id
        )

    return render_template("dashboard.html")


# create a blog post model
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    author = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    slug = db.Column(db.String(255))


# create a posts form
class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = StringField("Content", validators=[DataRequired()], widget=TextArea())
    author = StringField("Author", validators=[DataRequired()])
    slug = StringField("Slug", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route("/posts/delete/<int:id>")
def delete_post(id):
    post_to_delete = Posts.query.get_or_404(id)
    try:
        db.session.delete(post_to_delete)
        db.session.commit()
        flash("Blog post was deleted")
        # grab all posts from database
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template("posts.html", posts=posts)
    except:
        flash("Whoops! There was a problem deleting post. Please try again")


@app.route("/posts")
def posts():
    # grab all the post from the database
    posts = Posts.query.order_by(Posts.date_posted)
    return render_template("posts.html", posts=posts)


@app.route("/posts/<int:id>")
def post(id):
    post = Posts.query.get_or_404(id)
    return render_template("post.html", post=post)


@app.route("/posts/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_post(id):
    post = Posts.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.author = form.author.data
        post.slug = form.slug.data
        post.content = form.content.data

        # update database
        db.session.add(post)
        db.session.commit()
        flash("Post has been updated")
        return redirect(url_for("post", id=post.id))
    form.title.data = post.title
    form.author.data = post.author
    form.slug.data = post.slug
    form.content.data = post.content
    return render_template("edit_post.html", form=form)


@app.route("/add-post", methods=["GET", "POST"])
@login_required
def add_post():
    form = PostForm()

    if form.validate_on_submit():
        post = Posts(
            title=form.title.data,
            content=form.content.data,
            author=form.author.data,
            slug=form.slug.data,
        )
        # clear the form
        form.title.data = ""
        form.content.data = ""
        form.author.data = ""
        form.slug.data = ""

        # add post data to database
        db.session.add(post)
        db.session.commit()

        flash("Blog post has been submitted")

    # redirect to the webpage
    return render_template("add_post.html", form=form)


# json stuff
# @app.route("/date")
# def get_current_date():
#     favprite_pizza = {
#         "John": "peperoni",
#     }
#     return {"Date": date.today()}


# vid 8: crete a model
class Users(db.Model, UserMixin):  # inherit from db.Model
    id = db.Column(db.Integer, primary_key=True)  # primary key...
    username = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(200), nullable=False)  # nullable mean it cannot be empty
    email = db.Column(
        db.String(120), nullable=False, unique=True
    )  # unique means email must be unique
    favorite_color = db.Column(db.String(120))
    date_created = db.Column(
        db.DateTime, default=datetime.utcnow
    )  # default value is the current time

    # do some password stuff
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # change vertify to verify
    def vertify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # ceate a string
    def __repr__(self):
        return "<Name %r>" % self.name


@app.route("/delete/<int:id>")
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    name = None
    form = UserForm()
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User deleted successfully")
        our_users = Users.query.order_by(Users.date_created)
        return render_template(
            "add_user.html", form=form, name=name, our_users=our_users
        )
    except:
        flash("There was a problem deleting user, try again")
        return render_template(
            "add_user.html",
            form=form,
            name=name,
            our_users=our_users,
        )


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


# Update Database Record
@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form["name"]
        name_to_update.email = request.form["email"]
        name_to_update.favorite_color = request.form["favorite_color"]
        name_to_update.username = request.form["username"]
        try:
            db.session.commit()
            flash("User updated successfully!")
            return render_template(
                "update.html", form=form, name_to_update=name_to_update
            )
        except:
            flash("Error! Looks like there was a problem. Try again")
            return render_template(
                "update.html", form=form, name_to_update=name_to_update
            )
    else:
        return render_template(
            "update.html", form=form, name_to_update=name_to_update, id=id
        )


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


# vid 8
@app.route("/user/add", methods=["GET", "POST"])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(
            email=form.email.data
        ).first()  # check if the email is already in the database, return the first one or None if unquie
        if user is None:
            # Hash Password
            hashed_pw = generate_password_hash(
                form.password_hash.data, method="pbkdf2:sha256"
            )
            user = Users(
                username=form.username.data,
                name=form.name.data,
                email=form.email.data,
                favorite_color=form.favorite_color.data,
                password_hash=hashed_pw,
            )  # create a new user
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ""
        form.username.data = ""
        form.email.data = ""
        form.favorite_color.data = ""
        form.password_hash.data = ""
        flash("User added successfully")
    our_users = Users.query.order_by(
        Users.date_created
    )  # get all the users from the database
    return render_template("add_user.html", form=form, name=name, our_users=our_users)


# create a route decorator
@app.route("/")
def index():
    first_name = "John"
    stuff = "This is bold text"
    favorite_pizza = ["Pepperoni", "Cheese", "Mushroom"]
    return render_template(
        "index.html", first_name=first_name, stuff=stuff, favorite_pizza=favorite_pizza
    )


# localhost:5000/user/John
@app.route("/user/<name>")
def user(name):
    return render_template(
        "user.html", user_name=name
    )  # user_name can be accessed in template (.html)


# Custom Error Handling
# invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


# internal server error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500


@app.route("/test_pw", methods=["GET", "POST"])
def test_pw():
    email = None
    password = None
    pw_to_check = None
    passed = None
    form = PasswordForm()
    # validate the form
    if form.validate_on_submit():
        email = form.email.data
        password = form.password_hash.data
        # clear the form
        form.email.data = ""
        form.password_hash.data = ""
        flash("Form submitted successfully")

        # look up user by email
        pw_to_check = Users.query.filter_by(email=email).first()

        # check hash password
        passwed = check_password_hash(pw_to_check.password_hash, password)

    return render_template(
        "name.html",
        email=email,
        password=password,
        pw_to_check=pw_to_check,
        passed=passed,
        form=form,
    )


# create a route for name page
@app.route("/name", methods=["GET", "POST"])
def name():
    name = None
    form = NamerForm()
    # validate the form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ""
        flash("Form submitted successfully")

    return render_template("name.html", name=name, form=form)


if __name__ == "__main__":
    app.run(debug=True)
