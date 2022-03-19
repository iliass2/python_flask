from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from sqlalchemy import update
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SECRET_KEY'] = "random string"

mysql = SQLAlchemy(app)


class students(mysql.Model):
    id = mysql.Column('student_id', mysql.Integer, primary_key=True)
    username = mysql.Column(mysql.String(100))
    password = mysql.Column(mysql.String(50))
    email = mysql.Column(mysql.String(200))
    city = mysql.Column(mysql.String(10))
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        sessione = mysql.session()
        cursor = sessione.execute("SELECT * FROM students WHERE username ='" + username + "' AND password='"+password+"'").cursor
        account = cursor.fetchone()
        if account:
            for cc in account:
                print(cc)
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[1]
            msg = 'Logged in successfully !'
            return render_template('index.html', msg=msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'address' in request.form and 'city' in request.form and 'country' in request.form and 'postalcode' in request.form and 'organisation' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        organisation = request.form['organisation']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        postalcode = request.form['postalcode']
        session=mysql.session()
        cursor = session.execute("SELECT * FROM students WHERE username ='"+username+"'").cursor
       # cursor.execute('SELECT * FROM accounts WHERE username = % s', (username,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
          #   cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s, % s, % s, % s, % s, % s, % s)',
          #                 (username, password, email, organisation, address, city, state, country, postalcode,))
           # mysql.connection.commit()
           # msg = 'You have successfully registered !'
            student = students(username=username, password=password, email=email,city=city)

            mysql.session.add(student)
            mysql.session.commit()
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg=msg)


@app.route("/index")
def index():
    if 'loggedin' in session:
        return render_template("index.html")
    return redirect(url_for('login'))


@app.route("/display")
def display():
    if 'loggedin' in session:
        sessione = mysql.session()
        cursor = sessione.execute("SELECT * FROM students WHERE student_id =" + str(session['id']) + "").cursor

      #  cursor.execute('SELECT * FROM accounts WHERE id = % s', (session['id'],))
        account = cursor.fetchone()
        for acc in account:
            print(acc)
        return render_template("display.html", account=account)
    return redirect(url_for('login'))


@app.route("/update", methods=['GET', 'POST'])
def update():
    msg = ''
    if 'loggedin' in session:
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'address' in request.form and 'city' in request.form and 'country' in request.form and 'postalcode' in request.form and 'organisation' in request.form:
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            organisation = request.form['organisation']
            address = request.form['address']
            city = request.form['city']
            state = request.form['state']
            country = request.form['country']
            postalcode = request.form['postalcode']
            sessione = mysql.session()
            cursor = sessione.execute("SELECT * FROM students WHERE username ='" + username + "'").cursor

           # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            #cursor.execute('SELECT * FROM accounts WHERE username = % s', (username,))
            account = cursor.fetchone()
            if account:
                msg = 'Account already exists !'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address !'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'name must contain only characters and numbers !'
            else:
                x=sessione.query(students).get(session['id'])
             #   stmt = students.update().where(students.id == session['id']).values(username=username,password=password,email=email,city=city)
               # stmt=update().where(students.id==session['id']).values(username=username,password=password,email=email,city=city)
                x.username=username
                x.password=password
                x.email=email;
                x.city=city
                sessione.commit()
               # print(x.id)
            #    x.update({students.username:username,students.password:password,students.email:email})
                #sessione.execute(
                 #   'UPDATE students SET  username =% s, password =% s, email =% s,  city =% s WHERE id =% s',
                  #  (username, password, email,  city, (session['id'],),))
                mysql.session.commit()
                msg = 'You have successfully updated !'
        elif request.method == 'POST':
            msg = 'Please fill out the form !'
        return render_template("update.html", msg=msg)
    return redirect(url_for('login'))


if __name__ == "__main__":
    mysql.create_all()
    app.run(host="0.0.0.0", port=int("5000"))