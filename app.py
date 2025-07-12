from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
import traceback

app = Flask(__name__)

# ===== Absolute Path for SQLite DB (for Render) =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FOLDER = os.path.join(BASE_DIR, 'database')
DB_PATH = os.path.join(DB_FOLDER, 'students.db')


# ===== HOME PAGE =====
@app.route('/')
def home():
    return render_template('home.html')


# ===== COURSES PAGE =====
@app.route('/courses')
def courses():
    return render_template('courses.html')


# ===== FACULTY PAGE =====
@app.route('/faculty')
def faculty():
    return render_template('faculty.html')


# ===== CONTACT PAGE =====
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        if not os.path.exists(DB_FOLDER):
            os.makedirs(DB_FOLDER)

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        # Create messages table if it doesn't exist
        c.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                message TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        c.execute("INSERT INTO messages (name, email, message) VALUES (?, ?, ?)",
                  (name, email, message))
        conn.commit()
        conn.close()

        return redirect(url_for('home'))

    return render_template('contact.html')


# ===== REGISTER PAGE =====
@app.route('/register', methods=['GET', 'POST'])
def register():
    try:
        if request.method == 'POST':
            name = request.form['name']
            phone = request.form['phone']
            course = request.form['course']
            level = request.form['level']

            if not os.path.exists(DB_FOLDER):
                os.makedirs(DB_FOLDER)

            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()

            # Create students table if it doesn't exist
            c.execute('''
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    course TEXT,
                    level TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            c.execute("INSERT INTO students (name, phone, course, level) VALUES (?, ?, ?, ?)",
                      (name, phone, course, level))
            conn.commit()
            conn.close()

            return redirect(url_for('home'))

        return render_template('register.html')

    except Exception as e:
        return f"<h1>500 - Internal Server Error</h1><pre>{traceback.format_exc()}</pre>"


# ===== ADMIN LOGIN PAGE =====
@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Very simple check (you can upgrade to real login system later)
        if username == 'admin' and password == 'admin123':
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("SELECT * FROM students ORDER BY timestamp DESC")
            students = c.fetchall()
            c.execute("SELECT * FROM messages ORDER BY timestamp DESC")
            messages = c.fetchall()
            conn.close()
            return render_template('admin.html', students=students, messages=messages)
        else:
            return "<h3>Invalid admin credentials</h3>"

    return render_template('admin_login.html')