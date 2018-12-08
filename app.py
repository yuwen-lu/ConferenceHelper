from flask import Flask, render_template, flash, redirect, request, url_for, session, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt


app = Flask(__name__)

# config MySQL

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'conferenceassistant'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# init MySQL
mysql = MySQL(app)


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/countries')
def countries():
    country_list = [
        "China",
        "Germany",
        "France",
        "USA",
        "UK",
        "Russia",
    ]
    return render_template('country.html', country_list=country_list)


@app.route('/timer')
def timer():
    time = 300
    return render_template('timer.html', time=time)


@app.route('/timer/<int:num>s')
@app.route('/timer/<int:num>')
def customizeTimer(num):
    return render_template('timer.html', time=num)


@app.route('/about')
def about():
    return render_template('about.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password:', [
        validators.dataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')

    ])
    confirm = PasswordField('Confirm Password')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # create cursor
        cur = mysql.connection.cursor()

        cur.execute("insert into users(name, email, username, password)
                    values( % s, % s, % s, % s)", (name, email, usename, password))

        # commit to mysql db
        mysql.connection.commit()

        # close connection
        cur.close()

        flash('You are now registered and can log in', 'success')

        redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # get form fields
        username = request.form['username']
        password_candidate = request.form['password']

        # create db cursor
        cur = mysql.connection.cursor()

        # get user by username
        result = cur.execute(
            "select * from users where username= %s", [username])

        if result > 0:
            # get stored hash
            data = cur.fetchone()
            password = data['password']

            # compare passwords
            if sha256_crypt.verify(password_candidate, password):
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in!', 'success')
                return redirect(url_for('countries'))
            else:
                error = 'Invalid Login'
                return render_template('login.html', error=error)

            cur.close()
        else:
            error = 'User Not Found'
            return render_template('login.html', error=error)
    return render_template('login.html')


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True)
