from flask import Flask, render_template, url_for, redirect, request
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)
Bootstrap(app)

db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

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
    if request.method=='POST':
        form = request.form
        name = form['name']
        age = form['age']
        cur = mysql.connection.cursor()
        if cur.execute("INSERT INTO employee(name,age) VALUES(%s,%s)",(name,age)):
            mysql.connection.commit()
            return render_template("register.html", msg = "Registration Successful")

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

@app.errorhandler(404)
def page_not_found(e):
    return "Page not Found: "+str(e)

if __name__ == "__main__":
    app.run(debug=True, port=5001)