from flask import Flask, render_template, url_for, redirect, request, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
from datetime import datetime
from flask_ckeditor import CKEditor
import yaml
import logging
import os

app = Flask(__name__)
Bootstrap(app)
CKEditor(app)

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
    try:
        if request.method=='GET':
            cur = mysql.connection.cursor()
            result_blogs = cur.execute("SELECT * FROM blogs")
            if result_blogs > 0:
                blogs = cur.fetchall()
                return render_template("index.html", blogs=blogs)
            else:
                flash("Currently there is no blog to load",'info')
    except Exception as e:
        flash("An Unexpected error has occurred: "+str(e),'danger')

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
                    cur.close()
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
    if request.method == 'GET':
        try:
            cur = mysql.connection.cursor()
            username = session['username']
            querystring = "SELECT * FROM employee WHERE username = '{}'".format(username)
            result_user = cur.execute(querystring)
            if result_user == 1:
                emp = cur.fetchall()
                return render_template("settings.html", employee=emp)
        except Exception as e:
            flash("An Unexpected Exception has occurred: "+str(e),'danger')
    if request.method == 'POST':
        try:
            oldhashedpass = ""
            cur = mysql.connection.cursor()
            username = session['username']
            querystring = "SELECT * FROM employee WHERE username = '{}'".format(username)
            result_user = cur.execute(querystring)
            if result_user == 1:
                emp = cur.fetchall()
                oldhashedpass = emp[0]['password']
                _name = emp[0]['password']
                _age = emp[0]['age']
                _introduction = emp[0]['introduction']
            form = request.form
            username = session['username']
            print(username)
            name = form['name']

            oldpassword = form['oldpassword']
            print(oldpassword)
            newpassword = form['newpassword']
            print(newpassword)
            repassword = form['repassword']
            print(repassword)
            age = form['age']
            print(oldhashedpass)
            introduction = form['introduction']
            if check_password_hash(oldhashedpass,oldpassword)==False:
               flash("Current password is not valid!",'warning')
            else:
                if newpassword == repassword:
                    hashedPassword = generate_password_hash(newpassword)
                    if cur.execute("update employee set name = %s, age = %s, password = %s, introduction=%s where username = %s",(name,age, hashedPassword,introduction,username)):
                        mysql.connection.commit()
                        cur.close()
                        flash("Settings updated successfully. Please login again.",'success')
                    else:
                        flash("Faliled to update settings! Please try again later",'danger')
                else:
                    flash("New password didn't match!",'warning')
        except Exception as e:
            flash("An Unexpected Exception has occurred: "+str(e),'danger')
    return render_template('settings.html')

@app.route('/newblog',methods=['GET','POST'])
def newblog():
    try:
        if request.method == 'POST':
            form = request.form
            title = form['title']
            body = form['body']
            timeCreated = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            timeModified = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            user = str(session['username'])
            likes = 0
            category = form['category']
            cur = mysql.connection.cursor()
            #queryString = "INSERT INTO blogs(title,body,timecreated,timemodified,user,likes,category) VALUES({0},{1},'{2}','{3}','{4}',{5},{6})".format(title,body,timeCreated,timeModified,user,likes,category)
            #print(queryString)
            if cur.execute("INSERT INTO blogs(title,body,timecreated,timemodified,user,likes,category) VALUES(%s,%s,%s,%s,%s,%s,%s)",(title,body,timeCreated,timeModified,user,likes,category)):
                mysql.connection.commit()
                cur.close()
                flash("Your blog published Successfully",'success') 
            else:
                flash("Unable to create blog! Please try again",'danger')     

    except Exception as e:
        flash("Unable to create blog: "+str(e),'danger') 

    return render_template('newblog.html')

@app.route('/myblogs',methods=['GET','POST'])
def myblogs():
    if request.method=='GET':
        cur = mysql.connection.cursor()
        username = session['username']
        querystring = "SELECT * FROM blogs WHERE user = '{}'".format(username)
        result_user = cur.execute(querystring)
        if result_user > 0:
            userBlogs = cur.fetchall()
            cur.close()
            flash(str(result_user)+' blogs loaded successfully.','success')
            return render_template("myblogs.html", user_blogs=userBlogs)
        else:
            flash('You have not written any blog. Start writing now','info')

    return render_template("myblogs.html")

@app.route('/blog/<int:id>/')
def blog(id):
    if request.method=='GET':
        cur = mysql.connection.cursor()
        querystring = "SELECT * FROM blogs WHERE id = '{}'".format(id)
        result_blog = cur.execute(querystring)
        if result_blog > 0:
            userBlog = cur.fetchone()
            cur.close()
            flash(str(result_blog)+' blog loaded successfully.','success')
            return render_template("blog.html", blog=userBlog)
    return render_template("blog.html")

@app.route('/editblog/<int:id>/', methods=['GET','POST'])
def editblog(id):
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        title = request.form['title']
        body = request.form['body']
        timemodified = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        category = request.form['category']
        cur.execute("UPDATE blogs SET title = %s, body = %s, category = %s where id = %s",(title, body, category, id))
        mysql.connection.commit()
        cur.close()
        flash('Blog updated successfully', 'success')
        return redirect('/blog/{}/'.format(id))
    cur = mysql.connection.cursor()
    result_value = cur.execute("SELECT * FROM blogs WHERE id = {}".format(id))
    if result_value > 0:
        blog = cur.fetchone()
        blog_dict = {}
        blog_dict['title'] = blog['title']
        blog_dict['body'] = blog['body']
        blog_dict['category'] = blog['category']
        return render_template('editblog.html', blog=blog_dict)
    return render_template('editblog.html')

@app.route('/deleteblog/<int:id>/', methods=['GET','POST'])
def deleteblog(id):
    try:
        cur = mysql.connection.cursor()
        querystring = "DELETE FROM blogs WHERE id = {}".format(id)
        cur.execute(querystring)
        mysql.connection.commit()
        cur.close()
        flash('blog successfully deleted.','success')
        return redirect('myblogs.html')
    except Exception as e:
        flash('Failed to delete the blog: '+str(e), 'info')
    return redirect('myblogs.html')

@app.route('/logout',methods=['GET','POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.errorhandler(404)
def page_not_found(e):
    return "Page not Found: "+str(e)

if __name__ == "__main__":
    app.run(debug=True, port=5001)