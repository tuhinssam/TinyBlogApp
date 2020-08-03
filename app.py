from flask import Flask, render_template, url_for, redirect
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
mysql = MySQL(app)

@app.route('/')
def index():
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

@app.route('/about')
def about():
    #return "about page"
    return render_template("about.html")

@app.route('/css')
def css():
    return render_template('css.html')

if __name__ == "__main__":
    app.run(debug=True, port=5001)