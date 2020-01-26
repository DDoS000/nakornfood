from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from functools import wraps
import pyrebase

app = Flask(__name__)


# Use a service account
cred = credentials.Certificate('./static/nkornfood-firebase-adminsdk-jojhd-77cb198e46.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

fbConfig = {
  "apiKey": "AIzaSyAqrVYlAR6WWzU9qDAvhI8mxpGf_lCYcso",
  "authDomain": "nkornfood.firebaseapp.com",
  "databaseURL": "https://nkornfood.firebaseio.com",
  "projectId": "nkornfood",
  "storageBucket": "nkornfood.appspot.com",
  "messagingSenderId": "94762099297",
  "appId": "1:94762099297:web:ecde49d9f1d141233a8020",
  "measurementId": "G-HZRPLJLFZK"
}

firebase = pyrebase.initialize_app(fbConfig)
auth = firebase.auth()
database = firebase.database()

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Only Member, Please login !!!', 'danger')
            return redirect(url_for('login'))
    return wrap

@app.route('/')
def index():
    return render_template('login.html')


# Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
    return render_template('dashboard.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method =='POST':
        email = request.form['email']
        password = request.form['password']

        try:
            user = auth.sign_in_with_email_and_password(email,password)
            # Passed
            session['logged_in'] = True
            session['uid'] = user["localId"]
            session['email'] = user["email"]
            flash('You are now logged in', 'success')
            return redirect(url_for('dashboard'))
        except Exception as Error:
            print(Error)
            error = 'Wrong username or password !!!'
            return render_template('login.html',error=error)
    return render_template('login.html')

@app.route('/manage_store')
@is_logged_in
def manage_store():
    if request.method == 'POST':
    return render_template('manage_store.html')


# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.secret_key='DDoS'
    app.run(debug=True)


