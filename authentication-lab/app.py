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
    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    return render_template("add_tweet.html")




if __name__ == '__main__':
    app.run(debug=True)