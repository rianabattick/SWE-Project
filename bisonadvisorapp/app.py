from flask import Flask, render_template,url_for,request,redirect,g
import sqlite3
import requests
from loginpage import login, sign_up, database

app = Flask(__name__)

app.config['DATABASE'] = 'users.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

database()

#routes to main page
@app.route("/")
def homepage():
    return render_template("homepage.html")

#student login page
@app.route("/slogin", methods =["GET", "POST"] )
def student_login():

    error_message = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        #use data base connection
        conn = get_db()

        student = login(conn,username, password,"student")
        if student:
            return redirect(url_for('student_dashboard'))
        else:
            error_message = "Invalid username or password."

    return render_template("student-login.html",error_message=error_message )


#admin login page


@app.route("/alogin",  methods =["GET", "POST"])
def admin_login(): 
    error_message = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # use databse connection

        conn = get_db()

        admin = login(conn,username, password,"admin")
        if admin:
            return redirect(url_for('admin_dashboard'))
        else:
            error_message = "Invalid username or password."
 
    return render_template("admin-login.html",error_message=error_message )



#sign up page
@app.route("/signup",  methods =["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        usertype = request.form.get("accountType")

        # Use database connection
        conn = get_db()
        if usertype == "admin":
            sign_up(conn,username,password)
        if usertype == "student":
            sign_up(conn, username, password, usertype, first_name=request.form.get("firstName"), last_name=request.form.get("lastName"), student_id=request.form.get("studentID"), classification=request.form.get("classification"), gpa=request.form.get("gpa"), expected_graduation_date=request.form.get("expectedGradDate"))


        # Redirect back to homepage after successful sign-up
        return redirect(url_for('homepage'))

    return render_template("signup.html")

#chatbot
@app.route("/chatbot")
def chatbot():
    return render_template("AI-Engine.html")

'''

Do not modify above code ^^^^^


'''



# admin dashboard page (functionality needed*****)
@app.route('/admin_dashboard')
def admin_dashboard():
    return render_template('admin-dashboard.html')


#student dashboard page (functionality needed*****)
@app.route('/student_dashboard')
def student_dashboard():
    return render_template('student-dashboard.html')



#other pages need to be inserted here:
































if __name__ == "__main__":
    app.run(debug=True)