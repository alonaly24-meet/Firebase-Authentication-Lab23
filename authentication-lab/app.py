from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


config = { "apiKey": "AIzaSyCPENPTNkxNxTVBwVr-bJ9UfhNGFsr7Wwg","authDomain": "bibi-49330.firebaseapp.com","projectId": "bibi-49330","storageBucket": "bibi-49330.appspot.com","messagingSenderId": "582709654391",'appId': "1:582709654391:web:c2b2d562c00cc5afede772","measurementId": "G-YKRKPG041V", "databaseURL":"https://bibi-49330-default-rtdb.europe-west1.firebasedatabase.app/"}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

@app.route('/', methods=['GET', 'POST'])
def signin():
    if request.method=="POST":
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user']=auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
        except:
            return redirect(url_for("signin"))
    else:
        return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        full_name = request.form["full_name"]
        bio=request.form["bio"]
        username=request.form['username']
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get current timestamp

        user = { 'email': email,'password': password,'full_name': full_name,'username': username,'bio': bio}
        try:
            login_session['user']=auth.create_user_with_email_and_password(email, password)
            user_uid = login_session['user']['localId']
            db.child("Users").child(user_uid).set(user)
            return redirect(url_for('add_tweet'))
        except:
            return redirect(url_for("signup"))
    else:
        return render_template('signup.html')

def get_username(uid):
    UID=login_session['user']['localId'] 
    writer = db.child("Users").child(UID).get().val()
    return writer["username"]

@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method=="POST":
        text=request.form["text"]
        title=request.form["title"]
        uid = login_session['user']['localId']

        tweet = {'text': text,'title': title, 'uid': uid }
        new_tweet_key = db.child('Tweets').push(tweet)
        return redirect(url_for('all_tweets'))
    else:
        return render_template("add_tweet.html")


@app.route('/signout', methods=["GET","POST"])
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))

@app.route('/all_tweets', methods=["GET","POST"])
def all_tweets():
    tweets = db.child('Tweets').get().val()
    return render_template('tweets.html', tweets=tweets, get_username=get_username)

if __name__ == '__main__':
    app.run(debug=True)