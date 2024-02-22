from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
import os
import uuid
import logging
from flask_dance.contrib.google import make_google_blueprint, google

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'

# Create the 'uploads' folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.secret_key = 'Srihari'

google_bp = make_google_blueprint(client_id="your_client_id",
                                  client_secret="your_client_secret",
                                  redirect_to="google_login")

app.register_blueprint(google_bp, url_prefix="/login")


@app.route("/login/google")
def google_login():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v1/userinfo")
    assert resp.ok, resp.text
    return "You are {email} on Google".format(email=resp.json()["email"])

# Connect to the SQLite database
conn = sqlite3.connect('example.db')
cursor = conn.cursor()


# Close the connection
conn.close()

@app.route('/')
def first():
    if 'username' in session:  # Check if user is logged in
        username = session['username']
        # Fetch user information from the database using the username
        # Display the user's profile page
        try:
            # Connect to the SQLite database
            conn = sqlite3.connect('example.db')
            cursor = conn.cursor()

            # Retrieve User data
            cursor.execute("SELECT * FROM registrations WHERE username=?", (username,))
            User = cursor.fetchall()
            userData = User
            
            print(logging.debug(userData))
        

        except sqlite3.Error as e:
            print("SQLite error:", e)
            posts = []

        finally:
            # Close the connection
            conn.close()
        if User:  # Check if User list is not empty
            userData = User[0]
            return render_template('first.html', userData=userData)
        else:
            return render_template('first.html', userData=None)
    else:
        return render_template('first.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Connect to the SQLite database
        conn = sqlite3.connect('example.db')
        cursor = conn.cursor()

        # Query the database for the registrations
        cursor.execute("SELECT * FROM registrations WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        
        # Close the connection
        conn.close()

        if user:
            session['username'] = username  # Set session variable
            return redirect(url_for('home'))  # Redirect to home page after successful login
        else:
            return render_template('login.html', invalid_username=True)  # Render login page with error message
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        company_name = request.form['company_name']
        phone_number = request.form['phone_number']
        username = request.form['username']
        password = request.form['password']
        
        try:
            # Connect to the SQLite database
            conn = sqlite3.connect('example.db', timeout=10)
            cursor = conn.cursor()

            # Check if the username already exists
            cursor.execute("SELECT * FROM registrations WHERE username=?", (username,))
            existing_user = cursor.fetchone()
            
            if existing_user:
                # Username already exists, render the registration page with an error message
                return render_template('register.html', username_exists=True)

            # Insert the user into the registrations table
            cursor.execute("INSERT INTO registrations (first_name, last_name, company_name, phone_number, username, password) VALUES (?, ?, ?, ?, ?, ?)", 
                           (first_name, last_name, company_name, phone_number, username, password))
            
            # Commit the changes
            conn.commit()

            return redirect(url_for('login'))  # Redirect to login page after successful registration
        
        except sqlite3.Error as e:
            # Handle database errors
            print("SQLite error:", e)
        
        finally:
            # Close the connection in the finally block to ensure it's always closed
            if conn:
                conn.close()

    return render_template('register.html')


@app.route('/home')
def home():
    if 'username' in session:
        username = session['username']
        # Fetch user information from the database using the username
        # Display the user's profile page
        try:
            # Connect to the SQLite database
            conn = sqlite3.connect('example.db')
            cursor = conn.cursor()

            # Retrieve User data
            cursor.execute("SELECT * FROM registrations WHERE username=?", (username,))
            User = cursor.fetchall()
            userData = User[0]
            
            print(logging.debug(userData))
        

        except sqlite3.Error as e:
            print("SQLite error:", e)
            posts = []

        finally:
            # Close the connection
            conn.close()

        return render_template('home.html', userData=userData)
    else:
        return redirect(url_for('login'))

@app.route('/about')
def about():
    if 'username' in session:
        username = session['username']
        # Fetch user information from the database using the username
        # Display the user's profile page
        try:
            # Connect to the SQLite database
            conn = sqlite3.connect('example.db')
            cursor = conn.cursor()

            # Retrieve User data
            cursor.execute("SELECT * FROM registrations WHERE username=?", (username,))
            User = cursor.fetchall()
            userData = User[0]
            
            print(logging.debug(userData))
        

        except sqlite3.Error as e:
            print("SQLite error:", e)
            posts = []

        finally:
            # Close the connection
            conn.close()

    return render_template('about.html', userData=userData)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        company = request.form['company']
        message = request.form['message']

        try:
            # Connect to the SQLite database
            conn = sqlite3.connect('example.db')
            cursor = conn.cursor()

            # Create the "contact" table if it doesn't exist
            cursor.execute('''CREATE TABLE IF NOT EXISTS contact (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT,
                                email TEXT,
                                phone TEXT,
                                company TEXT,
                                message TEXT
                            )''')

            # Insert data into the "contact" table
            cursor.execute("INSERT INTO contact (name, email, phone, company, message) VALUES (?, ?, ?, ?, ?)", (name, email, phone, company, message))

            # Commit the changes
            conn.commit()

        except sqlite3.Error as e:
            print("SQLite error:", e)

        finally:
            # Close the connection
            conn.close()

    if 'username' in session:
        username = session['username']
        # Fetch user information from the database using the username
        # Display the user's profile page
        try:
            # Connect to the SQLite database
            conn = sqlite3.connect('example.db')
            cursor = conn.cursor()

            # Retrieve User data
            cursor.execute("SELECT * FROM registrations WHERE username=?", (username,))
            User = cursor.fetchall()
            userData = User[0]
            
            print(logging.debug(userData))
        

        except sqlite3.Error as e:
            print("SQLite error:", e)
            posts = []

        finally:
            # Close the connection
            conn.close()

    return render_template('contact.html', userData=userData)

@app.route('/gallery', methods=['GET', 'POST'])
def gallery():
    if request.method == 'POST':
        city = request.form['city']
        # Check if the post request has the file part
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return 'No selected file'
        if file:
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            try:
                # Connect to the SQLite database
                conn = sqlite3.connect('example.db')
                cursor = conn.cursor()

                # Insert data into the "gallery" table
                cursor.execute("INSERT INTO gallery (city, image) VALUES (?, ?)", (city, file_path))

                # Commit the changes
                conn.commit()

            except sqlite3.Error as e:
                print("SQLite error:", e)

            finally:
                # Close the connection
                conn.close()
    if 'username' in session:
        username = session['username']
        # Fetch user information from the database using the username
        # Display the user's profile page
        try:
            # Connect to the SQLite database
            conn = sqlite3.connect('example.db')
            cursor = conn.cursor()

            # Retrieve User data
            cursor.execute("SELECT * FROM registrations WHERE username=?", (username,))
            User = cursor.fetchall()
            userData = User[0]
            
            print(logging.debug(userData))
        

        except sqlite3.Error as e:
            print("SQLite error:", e)
            posts = []

        finally:
            # Close the connection
            conn.close()

    return render_template('gallery.html', userData=userData)

@app.route('/products')
def products():
    if 'username' in session:
        username = session['username']
        # Fetch user information from the database using the username
        # Display the user's profile page
        try:
            # Connect to the SQLite database
            conn = sqlite3.connect('example.db')
            cursor = conn.cursor()

            # Retrieve User data
            cursor.execute("SELECT * FROM registrations WHERE username=?", (username,))
            User = cursor.fetchall()
            userData = User[0]
            
            print(logging.debug(userData))
        

        except sqlite3.Error as e:
            print("SQLite error:", e)
            posts = []

        finally:
            # Close the connection
            conn.close()

    return render_template('products.html', userData=userData)

@app.route('/services')
def services():
    if 'username' in session:
        username = session['username']
        # Fetch user information from the database using the username
        # Display the user's profile page
        try:
            # Connect to the SQLite database
            conn = sqlite3.connect('example.db')
            cursor = conn.cursor()

            # Retrieve User data
            cursor.execute("SELECT * FROM registrations WHERE username=?", (username,))
            User = cursor.fetchall()
            userData = User[0]
            
            print(logging.debug(userData))
        

        except sqlite3.Error as e:
            print("SQLite error:", e)
            posts = []

        finally:
            # Close the connection
            conn.close()

    return render_template('services.html', userData=userData)

@app.route('/pricing')
def pricing():
    if 'username' in session:
        username = session['username']
        # Fetch user information from the database using the username
        # Display the user's profile page
        try:
            # Connect to the SQLite database
            conn = sqlite3.connect('example.db')
            cursor = conn.cursor()

            # Retrieve User data
            cursor.execute("SELECT * FROM registrations WHERE username=?", (username,))
            User = cursor.fetchall()
            userData = User[0]
            
            print(logging.debug(userData))
        

        except sqlite3.Error as e:
            print("SQLite error:", e)
            posts = []

        finally:
            # Close the connection
            conn.close()

    return render_template('pricing.html', userData=userData)

@app.route('/testimonials')
def testimonials():
    if 'username' in session:
        username = session['username']
        # Fetch user information from the database using the username
        # Display the user's profile page
        try:
            # Connect to the SQLite database
            conn = sqlite3.connect('example.db')
            cursor = conn.cursor()

            # Retrieve User data
            cursor.execute("SELECT * FROM registrations WHERE username=?", (username,))
            User = cursor.fetchall()
            userData = User[0]
            
            print(logging.debug(userData))
        

        except sqlite3.Error as e:
            print("SQLite error:", e)
            posts = []

        finally:
            # Close the connection
            conn.close()

    return render_template('testimonials.html', userData=userData)

@app.route('/careers')
def careers():
    if 'username' in session:
        username = session['username']
        # Fetch user information from the database using the username
        # Display the user's profile page
        try:
            # Connect to the SQLite database
            conn = sqlite3.connect('example.db')
            cursor = conn.cursor()

            # Retrieve User data
            cursor.execute("SELECT * FROM registrations WHERE username=?", (username,))
            User = cursor.fetchall()
            userData = User[0]
            
            print(logging.debug(userData))
        

        except sqlite3.Error as e:
            print("SQLite error:", e)
            posts = []

        finally:
            # Close the connection
            conn.close()

    return render_template('careers.html', userData=userData)

@app.route('/posts', methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':
        if 'username' in session:
            username = session['username']  # Fetch username from session
            caption = request.form['caption']
            image = request.files['image']

            # Save the image file and get the file path
            if image:
                filename = str(uuid.uuid4()) + os.path.splitext(image.filename)[1]
                image_path = os.path.join('static', 'uploads', filename)
                image.save(image_path)

                try:
                    # Connect to the SQLite database
                    conn = sqlite3.connect('example.db')
                    cursor = conn.cursor()

                    # Insert data into the "userposts" table
                    cursor.execute("INSERT INTO userposts (username, caption, image_url) VALUES (?, ?, ?)", (username, caption, image_path))

                    # Commit the changes
                    conn.commit()

                except sqlite3.Error as e:
                    print("SQLite error:", e)

                finally:
                    # Close the connection
                    conn.close()
    if 'username' in session:
        username = session['username']  # Fetch username from session
        # Fetch posts data from the database
        try:
            # Connect to the SQLite database
            conn = sqlite3.connect('example.db')
            cursor = conn.cursor()

            # Retrieve posts data
            cursor.execute("SELECT * FROM userposts WHERE username=?", (username,))
            posts = cursor.fetchall()
            
            print(logging.debug(posts))
            

        except sqlite3.Error as e:
            print("SQLite error:", e)
            posts = []

        finally:
            # Close the connection
            conn.close()

    try:
        conn = sqlite3.connect('example.db')
        cursor = conn.cursor()

        # Retrieve posts data
        cursor.execute("SELECT * FROM registrations")
        userList = cursor.fetchall()
        
        print(logging.debug(userList))
            

    except sqlite3.Error as e:
        print("SQLite error:", e)
        posts = []

    finally:
        # Close the connection
        conn.close()

    if 'username' in session:
        username = session['username']
        # Fetch user information from the database using the username
        # Display the user's profile page
        try:
            # Connect to the SQLite database
            conn = sqlite3.connect('example.db')
            cursor = conn.cursor()

            # Retrieve User data
            cursor.execute("SELECT * FROM registrations WHERE username=?", (username,))
            User = cursor.fetchall()
            userData = User[0]
            
            print(logging.debug(userData))
        

        except sqlite3.Error as e:
            print("SQLite error:", e)
            posts = []

        finally:
            # Close the connection
            conn.close()

    return render_template('posts.html', userData=userData, posts=posts, userList=userList)

@app.route('/<username>')
def user_details(username):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('example.db')
        cursor = conn.cursor()

        # Retrieve User data
        cursor.execute("SELECT * FROM registrations WHERE username=?", (username,))
        indiUserData = cursor.fetchall()
        indiUserDataList = indiUserData[0]
        
        print(logging.debug(indiUserData))
    
    except sqlite3.Error as e:
        print("SQLite error:", e)
        posts = []

    finally:
        # Close the connection
        conn.close()

    # Fetch posts data from the database
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('example.db')
        cursor = conn.cursor()

        # Retrieve posts data
        cursor.execute("SELECT * FROM userposts WHERE username=?", (username,))
        posts = cursor.fetchall()
        
        print(logging.debug(posts))
        

    except sqlite3.Error as e:
        print("SQLite error:", e)
        posts = []

    finally:
        # Close the connection
        conn.close()

    if 'username' in session:
        username = session['username']
        # Fetch user information from the database using the username
        # Display the user's profile page
        try:
            # Connect to the SQLite database
            conn = sqlite3.connect('example.db')
            cursor = conn.cursor()

            # Retrieve User data
            cursor.execute("SELECT * FROM registrations WHERE username=?", (username,))
            User = cursor.fetchall()
            userData = User[0]
            
            print(logging.debug(userData))
        

        except sqlite3.Error as e:
            print("SQLite error:", e)
            posts = []

        finally:
            # Close the connection
            conn.close()

    return render_template('userdetails.html', userData=userData, indiUserDataList=indiUserDataList, posts=posts)


@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove session variable
    return render_template('first.html')

if __name__ == '__main__':
    app.run(debug=True)
