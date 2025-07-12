from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

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

        conn = sqlite3.connect('database/students.db')
        c = conn.cursor()
        c.execute("INSERT INTO messages (name, email, message) VALUES (?, ?, ?)",
                  (name, email, message))
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

            # Ensure this path exists
            conn = sqlite3.connect('database/students.db')
            c = conn.cursor()
            c.execute("INSERT INTO students (name, phone, course, level) VALUES (?, ?, ?, ?)",
                      (name, phone, course, level))
            conn.commit()
            conn.close()

            return redirect(url_for('home'))

        return render_template('register.html')

    except Exception as e:
        # Show the exact error in the browser
        return f"<h1>500 - Internal Server Error</h1><p>{str(e)}</p>"
