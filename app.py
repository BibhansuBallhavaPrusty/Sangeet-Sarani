from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

DB_FOLDER = os.path.join(os.path.dirname(__file__), 'database')
DB_PATH = os.path.join(DB_FOLDER, 'students.db')

app = Flask(__name__)

# === HOME PAGE ===
@app.route('/')
def home():
    return render_template('home.html')

# === COURSES PAGE ===
@app.route('/courses')
def courses():
    return render_template('courses.html')

# === FACULTY PAGE ===
@app.route('/faculty')
def faculty():
    return render_template('faculty.html')

# === CONTACT PAGE ===
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        if not os.path.exists('database'):
            os.makedirs('database')

        conn = DB_PATH = os.path.join(os.path.dirname(__file__), 'database', 'students.db')
        sqlite3.connect(DB_PATH)
        c = conn.cursor()

        c.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                message TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        c.execute("INSERT INTO messages (name, email, message) VALUES (?, ?, ?)", (name, email, message))
        conn.commit()
        conn.close()

        return redirect(url_for('home'))

    return render_template('contact.html')


# === REGISTER PAGE ===
@app.route('/register', methods=['GET', 'POST'])
def register():
    try:
        if request.method == 'POST':
            name = request.form['name']
            phone = request.form['phone']
            course = request.form['course']
            level = request.form['level']

            if not os.path.exists('database'):
                os.makedirs('database')

            conn = DB_PATH = os.path.join(os.path.dirname(__file__), 'database', 'students.db')
            sqlite3.connect(DB_PATH)
            c = conn.cursor()

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
        import traceback
        return f"<h1>500 - Internal Server Error</h1><pre>{traceback.format_exc()}</pre>"


# === ADMIN LOGIN & DASHBOARD ===
@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # You can replace this with better auth later
        if username == 'admin' and password == 'password':
            return redirect(url_for('admin_dashboard'))
        else:
            return "<h3>Invalid credentials</h3>"

    return render_template('admin_login.html')


@app.route('/admin')
def admin_dashboard():
    conn = DB_PATH = os.path.join(os.path.dirname(__file__), 'database', 'students.db')
    sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT * FROM students")
    students = c.fetchall()

    c.execute("SELECT * FROM messages")
    messages = c.fetchall()

    conn.close()

    return render_template('admin.html', students=students, messages=messages)


# === DATABASE INITIALIZER FOR RENDER ===
@app.route('/init-db')
def init_db():
    if not os.path.exists('database'):
        os.makedirs('database')

    conn = DB_PATH = os.path.join(os.path.dirname(__file__), 'database', 'students.db')
    sqlite3.connect(DB_PATH)
    c = conn.cursor()

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

    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

    return "<h3>✅ Database initialized successfully on Render!</h3>"


# === RUN APP LOCALLY ===
if __name__ == '__main__':
    app.run(debug=True)