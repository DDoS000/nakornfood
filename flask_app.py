from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
import pyrebase

app = Flask(__name__)

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

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method =='POST':

        email = request.form['email']
        password = request.form['password']

        try:
            user = auth.sign_in_with_email_and_password(email,password)
            session['logged_in'] = True
            session['uid'] = user["idToken"]
        except Exception as Error:
            # error = str(Error)
            print("fall")
            return render_template('login.html')
    return render_template('loginpass.html')

if __name__ == '__main__':
    app.secret_key='DDoS'
    app.run(debug=True)
