from flask import Flask, render_template, session
from flask import render_template, url_for, flash, request, redirect, Response
import sqlite3
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from forms import LoginForm

#connect the SQLite Database as read-only
db = sqlite3.connect("file:database.db", check_same_thread=False, uri=True)
Cur = db.cursor()

app = Flask(__name__)

app.debug=True
login_manager = LoginManager(app)
login_manager.login_view = "login"

class User(UserMixin):
    def __init__(self, id, email, password, clerance):
        self.id = str(id)
        self.email = email
        self.password = password
        self.clerance = clerance
        self.authenticated = False    
        def is_active(self):
            return self.is_active()    
        def is_anonymous(self):
            return False    
        def is_authenticated(self):
            return self.authenticated    
        def is_active(self):
            return True    
        def get_id(self):
            return self.id
    
@login_manager.user_loader
def load_user(user_id):
   Cur.execute(f"SELECT * from UserDB where user_id = '{user_id}'")
   lu = Cur.fetchone()
   if lu is None:
      return None
   else:
      return User(int(lu[0]), lu[1], lu[2], lu[3])
   
@app.route("/login", methods=['GET','POST'])
def login():
  if current_user.is_authenticated:
     return redirect(url_for('Home'))
  form = LoginForm()
  if form.validate_on_submit():
     Cur.execute(f"SELECT * FROM UserDB where email = '{form.email.data}'")
     user = list(Cur.fetchone())
     Us = load_user(user[0])
     if form.email.data == Us.email and form.password.data == Us.password:
        login_user(Us, remember=form.remember.data)
        Umail = list({form.email.data})[0].split('@')[0]
        flash('Logged in successfully '+Umail)
        redirect(url_for('Home'))
     else:
        flash('Login Unsuccessfull.')
  return render_template('login.html',title='Login', form=form)


#create a simple route to the home page
@app.route("/")
def Home():
    return render_template('Home.html')

@app.route("/Table", methods=["GET", "POST"])
@login_required
def Table():
    listData = []
    fetch = Cur.execute(f"SELECT * FROM UserDB where user_id = '{session['user_id']}'")
    for lines in fetch:
        listData.append(lines)
    if listData[0][3] == 0:
        dataSelect = Cur.execute("SELECT * FROM Telenor")
    else:
        dataSelect = Cur.execute("SELECT * FROM Telenor Where BYGNINGSTYPE='111-Enebolig'")
    listData = []
    for lines in dataSelect:
        listData.append(lines)
    return render_template("Search.html", ListData=listData)

@app.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    return render_template('Home.html')

if __name__ == "__main__":
    app.secret_key = '9597975'
    app.run(debug=False)