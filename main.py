# Import necessary tools & features

import sqlite3
from gettext import install
from sqlite3 import Error
from flask import Flask, render_template, request, url_for, flash
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from werkzeug.utils import redirect

import re

from flask import Flask, render_template, jsonify


# DB file name
db_file = "mySQLite.db"

def create_connection():
    """ create a database connection to a SQLite database """
    conn = None
    try:
     conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
    def create_database():
        """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)

    # cursor object (to allow python to interact w/ DB)
        cursor = conn.cursor()

        # Drop the COMMENTSCOLOMBIA table if already exists.
        cursor.execute("DROP TABLE IF EXISTS COMMENTSCOLOMBIA")

        # Creating the COMMENTSBRAZIL table
        table = """CREATE TABLE COMMENTSCOLOMBIA (
                                     CommentId INTEGER PRIMARY KEY AUTOINCREMENT,
                                     Username VARCHAR(255) NOT NULL,
                                     Comment TEXT NOT NULL,
                                     FOREIGN KEY(Username) REFERENCES USER(Username)
                                 );"""
        cursor.execute(table)

        # Drop the COMMENTSBRAZIL table if already exists.

        cursor.execute("DROP TABLE IF EXISTS COMMENTSBRAZIL")

        # Creating COMMENTSBRAZIL table

        table = """CREATE TABLE COMMENTSBRAZIL (
                                     CommentId INTEGER PRIMARY KEY AUTOINCREMENT,
                                     Username VARCHAR(255) NOT NULL,
                                     Comment TEXT NOT NULL,
                                     FOREIGN KEY(Username) REFERENCES USER(Username)
                                 );"""
        cursor.execute(table)

        # Drop the COMMENTSGAL table if already exists.

        cursor.execute("DROP TABLE IF EXISTS COMMENTSGAL")

        # Creating COMMENTSGAL table

        table = """CREATE TABLE COMMENTSGAL (
                                             CommentId INTEGER PRIMARY KEY AUTOINCREMENT,
                                             Username VARCHAR(255) NOT NULL,
                                             Comment TEXT NOT NULL,
                                             FOREIGN KEY(Username) REFERENCES USER(Username)
                                         );"""
        cursor.execute(table)

        # Drop the USER table if already exists.
        cursor.execute("DROP TABLE IF EXISTS USER")
        # Creating USER table
        table = """ CREATE TABLE USER (
                                             Username VARCHAR(255) PRIMARY KEY,
                                             Password VARCHAR(255) NOT NULL,
                                             Email VARCHAR(255) NOT NULL,
                                             First_Name CHAR(25),
                                             Last_Name CHAR(25),
                                             Gender CHAR(25),
                                             Bio TEXT
                                         ); """
        cursor.execute(table)

        # Create KNOWN_LANGUAGES table
        cursor.execute("DROP TABLE IF EXISTS KNOWN_LANGUAGES")
        table = """ CREATE TABLE KNOWN_LANGUAGES (
                                                     Id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                     LanguageName VARCHAR(255),
                                                     Username INTEGER,
                                                     FOREIGN KEY(Username) REFERENCES USER(Username)
                                                 ); """
        cursor.execute(table)

        # Create FEEDBACK TABLE
        cursor.execute("DROP TABLE IF EXISTS FEEDBACK")
        table = """ CREATE TABLE FEEDBACK (
                                      Name VARCHAR(255),
                                      Email VARCHAR(255) NOT NULL,
                                      Feedback TEXT
                                  ); """
        cursor.execute(table)

        # Create stories TABLE
        cursor.execute("DROP TABLE IF EXISTS STORIES")
        table = """ CREATE TABLE STORIES (
                                        Name VARCHAR(255),
                                        Email VARCHAR(255) NOT NULL,
                                        Story TEXT
                                    ); """
        cursor.execute(table)




        conn.commit()
        print("Tables created successfully.")       #print when tables are created

    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


# Initialise flask app, set environment to dev, enable debug, set to "production" and false when website is launched
app = Flask(__name__)
app.config['ENV'] = "Development"
app.config['DEBUG'] = True

# Create bcyrpt object
bcrypt = Bcrypt(app)

# Create a LoginManager object

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'loginAction'

# User Class for the user that will be stored when the user is logged in
class User():
    def __init__(self, username):
         self.username = username
    def is_authenticated(self):
         return True
    def is_active(self):
         return True
    def is_anonymous(self):
         return False
    def get_id(self):
         return self.username

# route to html home page 'index'
@app.route('/')
def home():
    return render_template('index.html')

# Load user function
@login_manager.user_loader
def load_user(username):
    return User(username)

# Set a secret key for the login session
# a “secret key” also needed for the application to sign the cookies in a way similar to how a "salt" would be used to muddle a password before hashing
# to avoid attackers tempering the content of our cookies/creating illegitimate cookies
app.secret_key = '*£^*sjeycvrkAnJ^'


# route to signup page
@app.route('/signup')
def signup():
    return render_template("signup.html")

# Route to get in touch page
@app.route('/getintouch')
def getintouch():
    return render_template("getintouch.html")

# Route to tips page
@app.route('/traveltips')
def traveltips():
    return render_template("traveltips.html")

# Route to contact us page
@app.route('/contactus')
def countrymap():
    return render_template("contactus.html")

# Route to popular destinations page
@app.route('/popdestinations')
def popdestinations():
    return render_template("popdestinations.html")

# Route to travel stories page
@app.route('/travelstories')
def travelstories():
    return render_template("travelstories.html")

# Route to facts page
@app.route('/facts')
def facts():
    return render_template("facts.html")

# Route to brazil travel page
@app.route('/brazil')
def brazil():
    return render_template("brazil.html")

# Route to colombia travel page
@app.route('/colombia')
def colombia():
    return render_template("colombia.html")

# Route to feedback page
@app.route('/feedbackform')
def feedbackform():
    return render_template("feedbackform.html")

# Route to galapagos travel page
@app.route('/galapagos')
def galapagos():
    return render_template("galapagos.html")


@app.route('/signupAction', methods=['POST'])
def signupAction():
    # Variables initialised to empty so they will be ready to store user input received from the form
    username = ""
    password = ""
    email = ""
    fname = ""
    lname = ""
    gender = ""
    list_known_languages = []
    bio = ""
    # Retrieving form data, checking if fields are present in form submitted by user
    if request.form.get("username"):
        username = request.form.get("username")
    if request.form.get("password"):
        password = request.form.get("password")

        # Password is a normal string
        # Check if password meets requirements
        if len(password) < 10 or len(password) > 64:
            flash("Password must be between 10 and 64 characters long.")
            return redirect(url_for('signup'))

        if not re.search(r"[A-Z]", password) or not re.search(r"[a-z]", password) or not re.search(
                r"[!@#$%^&*()\-_=+{};:,<.>]", password):
            flash(
                "Password must contain at least one uppercase letter, one lowercase letter, and one special character.")
            return redirect(url_for('signup'))

        # Password is a normal string
        # Hash Password before putting it in the database (using the bcrypt object to hash)
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        print("True Password:", password, ", Hashed Password:", hashed_password)
        password = hashed_password

    # Retrieving form data, checking if fields are present in form submitted by user
    if request.form.get("email"):
        email = request.form.get("email")
    if request.form.get("fname"):
        fname = request.form.get("fname")
    if request.form.get("lname"):
        lname = request.form.get("lname")
    if request.form.get("gender"):
        gender = request.form.get("gender")
    if request.form.get("bio"):
        bio = request.form.get("bio")
    if request.form.get("selected_english"):
        list_known_languages.append("English")
    if request.form.get("selected_gaeilge"):
        list_known_languages.append("Gaeilge")
    if request.form.get("selected_french"):
        list_known_languages.append("French")
    if request.form.get("selected_spanish"):
        list_known_languages.append("Spanish")
    if request.form.get("selected_italian"):
        list_known_languages.append("Italian")

    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        myquery = "INSERT INTO USER (Username,Password,Email,First_Name,Last_Name,Gender,Bio) VALUES (?,?,?,?,?,?,?)"   #parameterised values to prevent SQL injection
        print("My query is: ", myquery)
        cursor.execute(myquery, (username, password, email, fname, lname, gender, bio))

        for languageName in list_known_languages:
            myquery = "INSERT INTO KNOWN_LANGUAGES (LanguageName,Username) VALUES (?,?)"    #parameterised values to prevent SQL injection
            print("My query is: ", myquery)
            cursor.execute(myquery,(languageName, username))
        conn.commit()
      ## if this works, this means the user have been added succesfully
        ## Therefore, we need to send them to the login page
    except Error as e:
        ## if the user is not added, we will get an exception which will be caught here
        #sign up was unsuccessful, tells user to try again
        flash("Failed to signup. Try again!")
        return redirect(url_for('signup'))
    finally:
        if conn:
            conn.close()   #close DB connection
    #account created, redirected to login page
    flash("Account created successfully.")
    return redirect(url_for('login'))

@app.route('/login')
def login():

    ## If user is already logged in we need to redirect them to their profile
    if current_user.is_authenticated:
        flash("You are already logged in.")
        return redirect(url_for('profile'))
    return render_template("login.html")

@app.route('/loginAction', methods=['POST'])
def loginAction():
    # Variables initialised to empty so they will be ready to store user input received from the form
    username=""
    password=""
    # Retrieving form data, checking if fields are present in form submitted by user
    if request.form.get("username"):
        username=request.form.get("username")
    if request.form.get("password"):
        password = request.form.get("password")
    try:
        conn = sqlite3.connect(db_file)     #connect to DB
        cursor = conn.cursor()              #create cursor(so python code can interact with DB)
        myquery="SELECT Password FROM USER WHERE Username='"+username+"'"       #SQL query to select password
        data=cursor.execute(myquery)
        passwordInDB=None
        for row in data:
            passwordInDB=row[0]
        if passwordInDB:

            ## We have found a username matching the one provide for the login
            ## Now, we need to check that the password provide for the login is also correct
            validPassword = bcrypt.check_password_hash(passwordInDB, password)


            ## If the passwords match, we need to mark them as logged in and send them to their profile
            ## Else we need to send them to the login page again
            if validPassword:
                login_user(User(username))
                flash("You are now logged in.")
                return redirect(url_for('profile'))
            else:

                ## The Username does not exist
                ## we need to send them to the login page again
                flash("Your username/password is incorrect! Try to login again.")
                return redirect(url_for('login'))
    except Error as e:
        ## if there was an error in the login, we will get an exception which will be caught here
        ## So we need to send the user to the login page again
        flash("Failed to login. Try again!")
        return redirect(url_for('login'))
    finally:
        if conn:
            conn.close()
    flash("You are now logged in.")
    return redirect(url_for('profile'))


@app.route('/profile', methods=['GET'])
def profile():

    ## If the user is not logged in, we need to redirect them to the login page
    if not (current_user.is_authenticated):
        flash("You need to login to access the profile page.")
        return redirect(url_for('login'))


    ## If the user is logged in, we need to get their username
    myusername = current_user.username


    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        myemail=""
        myfname=""
        mylname=""
        mygender=""
        mybio=""
        myknown_languages=[]
        # Get the personal data of the user
        myquery="SELECT Email, First_Name, Last_Name, Gender, Bio FROM USER WHERE Username='"+myusername+"'"
        dataUser = cursor.execute(myquery)
        print("These are the details of the user: ")
        rows=[]
        for row in dataUser:
            print(row)
            rows.append(row)
        if len(rows)==1:
            myemail=rows[0][0]
            myfname=rows[0][1]
            mylname=rows[0][2]
            mygender=rows[0][3]
            mybio=rows[0][4]
        else:
            return "Error: the Username does not exist"

        # Get the know languages of the User
        myquery = "SELECT LanguageName FROM KNOWN_LANGUAGES WHERE Username='" + myusername + "'"
        dataUser = cursor.execute(myquery)
        print("These are the user's known languages: ")
        for row in dataUser:
            print(row)
            myknown_languages.append(row[0])
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()    #close connection to database

    # the data of the user is included in this render, so it is retrieved from the database
    return render_template("profile.html", username=myusername,email=myemail,fname=myfname,lname=mylname, gender=mygender,known_languages=myknown_languages,bio=mybio)


@app.route('/update_profile', methods=['GET', 'POST'])
@login_required  # Ensure the user is logged in to access this route
def update_profile():

    if request.method == 'POST':
        # Extract updated information from the form
        email = request.form.get('email')
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        gender = request.form.get('gender')
        bio = request.form.get('bio')

        # Update the user's information in the database
        try:
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            cursor.execute("UPDATE USER SET Email=?, First_Name=?, Last_Name=?, Gender=?, Bio=? WHERE Username=?",
                           (email, fname, lname, gender, bio, current_user.username))
            conn.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('profile'))
        except Error as e:
            print(e)
            flash('Failed to update profile. Please try again.', 'error')
        finally:
            if conn:
                conn.close()

    # Render the update profile form
    return render_template('update_profile.html')

#function to logout user
@app.route("/logout")
def logout():

    ## If the user is logged in, then logout the user
    if current_user.is_authenticated:
        logout_user()
    flash("Logout successful.")
    return redirect(url_for('login'))

# Add this route to your Flask application
@app.route('/delete_account', methods=['POST'])
@login_required  # Requires the user to be logged in to access this route
def delete_account():
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Get the username of the current user
        username = current_user.username

        # Delete user from the USER table
        cursor.execute("DELETE FROM USER WHERE Username=?", (username,))

        # Commit changes to database
        conn.commit()

        # Logout the user after deleting their account
        logout_user()

        flash('Your account has been deleted successfully.', 'success')
    except Error as e:
        print(e)
        flash('An error occurred while deleting your account. Please try again.', 'error')
    finally:
        if conn:
            conn.close()

    return redirect(url_for('home'))  # Redirect to the home page after deleting the account


#to insert user input to feedback table, create connection & execute SQL query
@app.route('/feedback', methods=['POST'])
def submit_feedback():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        feedback = request.form['feedback']

        # Connect to SQLite database
        conn = sqlite3.connect('mySQLite.db')
        cursor = conn.cursor()

        # Insert data into feedback table
        cursor.execute("INSERT INTO feedback (name, email, feedback) VALUES (?, ?, ?)", (name, email, feedback))    #parameterised values to prevent SQL injection
        conn.commit()

        cursor.close()
        conn.close()

        flash('Feedback submitted successfully!', 'success')  # Flash success message
    else:
        flash('Feedback submission failed.', 'error')  # Flash error message

    return redirect(url_for('feedbackform'))        #return to feedback page


#to insert user input to stories table, create connection & execute SQL query
@app.route('/story', methods=['POST'])
def submit_story():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        story = request.form['story']

        # Connect to SQLite database
        conn = sqlite3.connect('mySQLite.db')
        cursor = conn.cursor()

        # Insert data into story table
        cursor.execute("INSERT INTO stories (name, email, story) VALUES (?, ?, ?)", (name, email, story))   #parameterised values to prevent SQL injection
        conn.commit()

        cursor.close()
        conn.close()    #close connection after finishing using the database

        flash('Story submitted successfully!', 'success')  # Flash success message
    else:
        flash('Story submission failed.', 'error')  # Flash error message

    return redirect(url_for('travelstories'))       #return to story entry page

#check user is authenticated before they attempt to leave a comment (only users can leave comments)
@app.route('/submit_comment_colombia', methods=['POST'])
def submit_comment_colombia():
    if current_user.is_authenticated:
        username = current_user.username
        comment = request.form.get('comment')

        # to insert values to commentscolombia table, create connection & execute SQL query
        try:
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO COMMENTSCOLOMBIA (Username, Comment) VALUES (?, ?)", (username, comment))   #parameterised values to prevent SQL injection
            conn.commit()
            flash('Comment submitted successfully!', 'success')  # Flash success message
        except Error as e:
            print(e)
            flash('An error occurred while submitting the comment.', 'error')  # Flash error message
        finally:
            if conn:
                conn.close()

        # Redirect back to the page from where the request was made
        return redirect(request.referrer)
    else:
        flash('You need to login to submit a comment.', 'error')  # Flash error message
        return redirect(url_for('login'))  # Redirect to login page


def get_comments_colombia():
    try:
        conn = sqlite3.connect(db_file)     #create connection to db
        cursor = conn.cursor()              #create cursor
        cursor.execute("SELECT Username, Comment FROM COMMENTSCOLOMBIA")    #use cursor to select usernames & comments from the colombia comments table
        comments = cursor.fetchall()
    except Error as e:
        print(e)            #print errors
        comments = []       #if errors found, set comments to empty
    finally:
        if conn:
            conn.close()    #close connection
    return comments         #return comments

@app.route('/get_colombia_comments')
def get_colombia_comments():
    comments = get_comments_colombia()  # comments variable = comments returned from get_comments_colombia function
    return jsonify(comments)  # Convert comments to JSON to post to page (for readability)




#check user is authenticated before they attempt to leave a comment (only users can leave comments)
@app.route('/submit_comment_brazil', methods=['POST'])
def submit_comment_brazil():
    if current_user.is_authenticated:   #if user is authenticated
        username = current_user.username        #username & comment user submits are both stored in the brazil comments database
        comment = request.form.get('comment')

        #to insert values(comments) to commentsbrazil table, create connection & execute SQL query
        try:
            conn = sqlite3.connect(db_file)     #create connection to DB
            cursor = conn.cursor()              #create cursor (to allow python code to interact w/ DB)
            cursor.execute("INSERT INTO COMMENTSBRAZIL (Username, Comment) VALUES (?, ?)", (username, comment)) #parameterised values to prevent SQL injection
            conn.commit()
            flash('Comment submitted successfully!', 'success')  # Flash success message if comment is submitted
        except Error as e:
            print(e)            #print errors
            flash('An error occurred while submitting the comment.', 'error')  # Flash error message if failed
        finally:
            if conn:
                conn.close()       #close connection to DB

        # Redirect back to the page from where the request was made
        return redirect(request.referrer)
    else:
        flash('You need to login to submit a comment.', 'error')  # Flash error message if user is not logged in
        return redirect(url_for('login'))  # & redirect to login page

#@app.route('/fetch_comments_brazil')
#def fetch_comments_brazil():
#    comments = get_comments_brazil()
#    return render_template('brazil.html', comments=comments)

def get_comments_brazil():
    try:
        conn = sqlite3.connect(db_file)     #create connection with DB
        cursor = conn.cursor()              #create cursor (to allow python code to interact w/ DB)
        cursor.execute("SELECT Username, Comment FROM COMMENTSBRAZIL")
        comments = cursor.fetchall()    #retrieve all from DB
    except Error as e:      #error handling
        print(e)            #print errors
        comments = []       #if error found, set comments to empty
    finally:
        if conn:
            conn.close()    #close DB connection
    return comments         #return comments from DB

@app.route('/get_brazil_comments')
def get_brazil_comments():
    comments = get_comments_brazil()  # comments variable = comments returned from get_comments_brazil function
    return jsonify(comments)  # Convert comments to JSON to post to page (for readability)

#check user is authenticated before they attempt to leave a comment (only users can leave comments)
@app.route('/submit_comment_gal', methods=['POST'])
def submit_comment_gal():
    if current_user.is_authenticated:   #if user is authenticated
        username = current_user.username
        comment = request.form.get('comment')

        #to insert values(comments) to commentsgal table, create connection & execute SQL query
        try:
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO COMMENTSGAL (Username, Comment) VALUES (?, ?)", (username, comment))    #parameterised values to prevent SQL injection
            conn.commit()
            flash('Comment submitted successfully!', 'success')  # Flash success message
        except Error as e:
            print(e)
            flash('An error occurred while submitting the comment.', 'error')  # Flash error message
        finally:
            if conn:
                conn.close()    #close DB connection

        # Redirect back to the page from where the request was made
        return redirect(request.referrer)
    else:
        flash('You need to login to submit a comment.', 'error')  # Flash error message
        return redirect(url_for('login'))  # Redirect to login page


def get_comments_gal():
    try:
        conn = sqlite3.connect(db_file)     #create DB connection
        cursor = conn.cursor()              #create cursor (object python code uses to interact with DB)
        cursor.execute("SELECT Username, Comment FROM COMMENTSGAL")     #select from DB (SQL)
        comments = cursor.fetchall()        #retrieve from DB
    except Error as e:                  #error handling
        print(e)                     #print errors
        comments = []               #set comments to empty if error occurs
    finally:
        if conn:
            conn.close()    #close connection
    return comments         #return comments from DB

@app.route('/get_gal_comments')
def get_gal_comments():
    comments = get_comments_gal()  # comments= comments returned from get_comments_gal function
    return jsonify(comments)  # Convert comments to JSON for readability




if __name__ == '__main__':

   # create_connection() # Called to also call create_database() function to create tables in database

    app.run(debug=True)

