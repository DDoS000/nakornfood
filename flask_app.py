from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from functools import wraps
import pyrebase

app = Flask(__name__)


# Use a service account
cred = credentials.Certificate(
    './static/foodmanage-e63a1-firebase-adminsdk-jvifj-bda07ba578.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

fbConfig = {
    "apiKey": "AIzaSyAX5UAWd54SOE-YHO57YWOgMLlJ2bmgcn8",
    "authDomain": "foodmanage-e63a1.firebaseapp.com",
    "databaseURL": "https://foodmanage-e63a1.firebaseio.com",
    "projectId": "foodmanage-e63a1",
    "storageBucket": "foodmanage-e63a1.appspot.com",
    "messagingSenderId": "1024309103110",
    "appId": "1:1024309103110:web:5895822a1b04b8a9ffd187"
}

firebase = pyrebase.initialize_app(fbConfig)
auth = firebase.auth()
database = firebase.database()


def GetDataUser(uid):
    doc_ref = db.collection(u'users').document(uid)
    doc = doc_ref.get()
    docs = doc.to_dict()
    return docs


# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrap


@app.route('/')
def index():
    if 'logged_in' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')


# Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
    return render_template('dashboard.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'logged_in' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            user = auth.sign_in_with_email_and_password(email, password)
            # Passed
            docs = GetDataUser(user["localId"])
            print(docs)
            if docs["acc"]["manage"] == True:
                session['logged_in'] = True
                session['uid'] = user["localId"]
                session['email'] = user["email"]
                session['storename'] = docs["store"]["storename"]
                flash('เข้าสู้ระบบสําเร็จ', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('คุณไม่มีสิทธิ์เข้าถึง', 'success')
                return redirect(url_for('dashboard'))
        except Exception as Error:
            print(Error)
            error = 'อีเมลล์หรือรหัสผ่านไม่ถูกต้อง'
            return render_template('login.html', error=error)
    return render_template('login.html')


@app.route('/manageStore/', methods=['GET', 'POST'])
@is_logged_in
def manageStore():
    docs = GetDataUser(session['uid'])
    try:
        session['storename'] = docs["store"]["storename"]
        storename = docs["store"]["storename"]
        desc = docs["store"]["desc"]
        Open = docs["store"]["time"]["open"]
        close = docs["store"]["time"]["close"]
        lat = docs["store"]["location"]["lat"]
        lng = docs["store"]["location"]["lng"]
    except Exception:
        print(u'No such document!')
        storename = ""
        desc = ""
        Open = ""
        close = ""
        lat = 0
        lng = 0

    if request.method == "POST":
        storename = request.form['storename']
        desc = request.form['desc']
        Open = request.form['open']
        close = request.form['close']
        lat = request.form['lat']
        lng = request.form['lng']
        data = {
            u"store": {
                u"storename": str(storename),
                u"desc": str(desc),
                u"time": {
                    u"open": str(Open),
                    u"close": str(close)
                },
                u"location": {
                    u"lat": float(lat),
                    u"lng": float(lng)
                }
            }
        }
        session['storename'] = storename
        try:
            db.collection(u'users').document(session['uid']).update(data)
            flash('อัพเดทข้อมูลสําเร็จ', 'success')
            return render_template('manageStore.html', storename=storename, desc=desc, Open=Open, close=close, lat=lat, lng=lng)
        except KeyError:
            print(KeyError)
            return render_template('manageStore.html', storename=storename, desc=desc, Open=Open, close=close, lat=lat, lng=lng)
    return render_template('manageStore.html', storename=storename, desc=desc, Open=Open, close=close, lat=lat, lng=lng)


@app.route('/manageFood/', methods=['GET', 'POST'])
def manageFood():
    try:
        docs = GetDataUser(session['uid'])
        count = (docs["manu"]["count"]) + 1
        print(count)
    except Exception:
        print(u'No such document!')
        count = 0

    if request.method == "POST":
        foodname = request.form['foodname']
        detail = request.form['foodedtail']
        price = request.form['foodprice']
        url = request.form['url']
        print("setdata")
        data = {
            u"manu": {
                u"count": count,
                f"uid:{count}": {
                    u"name": foodname,
                    u"detail": detail,
                    u"price": price,
                    u"photourl": url,
                }
            },
        }
        try:
            db.collection(u'users').document(session['uid']).update(data)
            print("updata")
            flash('อัพเดทข้อมูลสําเร็จ', 'success')
        except KeyError:
            print(KeyError)
    return render_template('manageFood.html')


@app.route('/manageSeat')
def manageSeat():
    return render_template('manageSeat.html')


# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('ออกจากระบบสําเร็จ', 'success')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.secret_key = 'DDoS'
    app.run(debug=True)
