from flask import Flask, render_template, redirect, url_for, request, flash
import psycopg2
import psycopg2.extras

from sqlalchemy import create_engine
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

engine = create_engine(
    "postgresql://postgres:Friends02@localhost:5432/inate")
db = scoped_session(sessionmaker(bind=engine))

# use decorators to link the function to a url


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/welcome')
def welcome():
    return render_template('welcome.html')


# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


@app.route('/register', methods=['POST', 'GET'])
def register():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form.get('username')
        password = request.form.get('password')

        cursor.execute(
            'SELECT * FROM employee WHERE username = %s', (username,))
        account = cursor.fetchone()
        print(account)

        if account:
            flash('Account already exists!')
        else:
            cursor.execute(
                "INSERT INTO employee(username, password) VALUES (%s,%s)", (username, password))
            conn.commit()
            flash('Register Success!')

    return render_template('register.html')


# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)
