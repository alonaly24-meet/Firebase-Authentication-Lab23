from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


config = { "apiKey": "AIzaSyCPENPTNkxNxTVBwVr-bJ9UfhNGFsr7Wwg",
  "authDomain": "bibi-49330.firebaseapp.com",
  "projectId": "bibi-49330",
  "storageBucket": "bibi-49330.appspot.com",
  "messagingSenderId": "582709654391",
  'appId': "1:582709654391:web:c2b2d562c00cc5afede772",
  "measurementId": "G-YKRKPG041V", "databaseURL":""}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()


@app.route('/', methods=['GET', 'POST'])
def signin():
    if request.method=="POST":
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user']=auth.create_user_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
        except:
            return redirect(url_for("signin"))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user']=auth.create_user_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
        except:
            return redirect(url_for("signup"))



@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    return render_template("add_tweet.html")

@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))




if __name__ == '__main__':
    app.run(debug=True)