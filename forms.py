from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import sqlite3

db = sqlite3.connect("file:database.db", check_same_thread=False, uri=True)
Cur = db.cursor()

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login') 
    def validate_email(self, email):
        Cur.execute(f"SELECT email FROM UserDB where email='{email.data}'")
        valemail = Cur.fetchone()
        if valemail is None:
            raise ValidationError('This Email ID is not registered. Please register before login')