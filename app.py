from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
import os
import uuid
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'

# Create the 'uploads' folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.secret_key = 'Srihari'

# Connect to the SQLite database
conn = sqlite3.connect('example.db')
cursor = conn.cursor()


# Close the connection
conn.close()

@app.route('/')
def first():
    if 'username' in session:  # Check if user is logged in
        return render_template('home.html')
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

        # Query the database for the user
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
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
        username = request.form['username']
        password = request.form['password']
        
        try:
            # Connect to the SQLite database
            conn = sqlite3.connect('example.db', timeout=10)
            cursor = conn.cursor()

            # Check if the username already exists
            cursor.execute("SELECT * FROM Users WHERE username=?", (username,))
            existing_user = cursor.fetchone()
            
            if existing_user:
                # Username already exists, render the registration page with an error message
                return render_template('register.html', username_exists=True)

            # Insert the user into the users table
            cursor.execute("INSERT INTO Users (username, password) VALUES (?, ?)", (username, password))
            
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
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

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

    return render_template('contact.html')

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

    return render_template('gallery.html')

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

@app.route('/testimonials')
def testimonials():
    return render_template('testimonials.html')

@app.route('/careers')
def careers():
    return render_template('careers.html')

@app.route('/posts', methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':
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

                # Insert data into the "posts" table
                cursor.execute("INSERT INTO posts (caption, image_url) VALUES (?, ?)", (caption, image_path))

                # Commit the changes
                conn.commit()

            except sqlite3.Error as e:
                print("SQLite error:", e)

            finally:
                # Close the connection
                conn.close()

    # Fetch posts data from the database
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('example.db')
        cursor = conn.cursor()

        # Retrieve posts data
        cursor.execute("SELECT * FROM posts")
        posts = cursor.fetchall()
        
        print(logging.debug(posts))
        

    except sqlite3.Error as e:
        print("SQLite error:", e)
        posts = []

    finally:
        # Close the connection
        conn.close()

    return render_template('posts.html', posts=posts)

@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove session variable
    return render_template('first.html')

if __name__ == '__main__':
    app.run(debug=True)
