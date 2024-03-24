from flask import Flask, render_template

# create a flask instance by calling app
app = Flask(__name__)

# create a route decorator
@app.route('/')
def index():
    return render_template('index.html')

# localhost:5000/user/John
@app.route('/user/name')
def user(name):
    return render_template('user.html', user_name=name) # user_name can be accessed in template (.html)

# Custom Error Handling
# invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# internal server error
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500
