from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import psycopg2
import psycopg2.extras

import sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

app.secret_key = '12345678'
# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

DB_HOST = 'localhost'
DB_NAME = 'inate'
DB_USER = 'postgres'
DB_PASS = 'Friends02'
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER,
                        password=DB_PASS, host=DB_HOST)


# use decorators to link the function to a url


@app.route('/')
def home():

    if 'loggedin' in session:

        return render_template('home.html', username=session['username'])

    return render_template('home.html')


@app.route('/welcome')
def welcome():
    return render_template('welcome.html')


# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    error = None
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        print(username)
        print(password)

        cursor.execute(
            'SELECT * FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()

        if account:
            password_rs = account['password']
            print(password_rs)

            if password_rs:
                session['loggedin'] = True
                session['id'] = account['id']
                session['username'] = account['username']

                return redirect(url_for('home'))
            else:
                flash('Incorrect Username/Password')

        else:
            flash('Incorrect Username/Password')

    return render_template('login.html', error=error)


@app.route('/register', methods=['POST', 'GET'])
def register():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form.get('username')
        password = request.form.get('password')

        cursor.execute(
            'SELECT * FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()
        print(account)

        if account:
            flash('Account already exists!')
        else:
            cursor.execute(
                "INSERT INTO users(username, password) VALUES (%s,%s)", (username, password))
            conn.commit()
            flash('Register Success!')

    return render_template('register.html')


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)
