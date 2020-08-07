from flask import Flask, render_template, url_for, redirect, request, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
import yaml
import logging
import os

app = Flask(__name__)
Bootstrap(app)

db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

app.config['SECRET_KEY'] = os.urandom(24) #this is required for creating session var

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        return "password: "+request.form['password']+" successfully submitted."
    cur = mysql.connection.cursor()
    #cur.execute("INSERT INTO user VALUES(%s)",['Mike'])
    #mysql.connection.commit()
    result_user = cur.execute("SELECT * FROM user")
    if result_user > 0:
        users = cur.fetchall()
        print(users)
    return render_template('index.html')

@app.route('/index1')
def index1():
    fruitsList = ['apple','mango', 'pear']
    #return redirect(url_for('about'))
    return render_template("index1.html", fruits = fruitsList)
    #return "Hello World!"

@app.route('/adduser', methods=['GET'])
def add_user():
    cur = mysql.connection.cursor()
    if cur.execute("INSERT INTO user(user_name) VALUES('Rahul')"):
        mysql.connection.commit()
        return 'success', 201
    render_template('index.html')

@app.route('/register', methods=['GET','POST'])
def register():
    try:
        if request.method=='POST':
            form = request.form
            name = form['name']
            username = form['username']
            password = form['password'] 
            repassword = form['repassword']
            age = form['age']
            introduction = form['introduction']
            if (password == repassword):
                cur = mysql.connection.cursor()
                #password hashing
                hashed_password = generate_password_hash(password)
                if cur.execute("INSERT INTO employee(name,age,username,password,introduction) VALUES(%s,%s,%s,%s,%s)",(name,age, username,hashed_password,introduction)):
                    mysql.connection.commit()
                    flash("User successfully registered. Please login to continue",'success')
                    return redirect(url_for('login'))
                else:
                    flash("Unable to Register user! Please try again",'danger')
                    #return render_template("register.html", msg = "Password didn't match")
            else:
                flash("Password didn't match!",'danger')

                    
    except Exception as e:
        print(e)
        flash("Registration Unsuccessful: "+str(e),'danger')
        return render_template('register.html', msg = "Registration Unsuccessful!")

    return render_template("register.html")

@app.route('/employee', methods=['GET','POST'])
def employee():
    if request.method=='GET':
        cur = mysql.connection.cursor()
        result_user = cur.execute("SELECT * FROM employee")
        if result_user > 0:
            emp = cur.fetchall()
            return render_template("employee.html", employee=emp)

    return render_template("employee.html")

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        try:
            form = request.form
            username = form['username']
            password = form['password']
            cur = mysql.connection.cursor()
            querystring = "SELECT * FROM employee WHERE username = '{}'".format(username)
            print(querystring)
            result_user = cur.execute(querystring)
            if result_user == 1:
                result = cur.fetchall()
                print("name: "+str(result[0]['name']))
                #print(result[0]['password'])
                if check_password_hash(result[0]['password'],password)==True:
                    session['name'] = str(result[0]['name'])
                    session['username'] = username
                    
                    return redirect(url_for('employee'))
                else:
                    flash('Login Failed! Please check your username or password','danger')
                    return render_template("login.html",msg = "Login Failed! Please check your username or password")
            else:
                return render_template("login.html",msg = "Login Failed! Please check your username or password")
        except Exception as e:
            flash("login Unsuccessful: "+str(e),'danger')
            print("Error in login:"+str(e))
            return render_template("login.html")

    return render_template("login.html")

@app.route('/settings',methods=['GET','POST'])
def settings():
    return render_template('settings.html')

@app.route('/newblog',methods=['GET','POST'])
def newblog():
    return render_template('newblog.html')

@app.route('/logout',methods=['GET','POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.errorhandler(404)
def page_not_found(e):
    return "Page not Found: "+str(e)

if __name__ == "__main__":
    app.run(debug=True, port=5001)