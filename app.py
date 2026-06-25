import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
DB_NAME = 'lms.db'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS courses (id INTEGER PRIMARY KEY, name TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY, name TEXT, course_id INTEGER)')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = get_db_connection()
    courses = conn.execute('SELECT * FROM courses').fetchall()
    # Talabalarni kurs nomi bilan qo'shib olish
    students = conn.execute('''
        SELECT students.name as student_name, courses.name as course_name 
        FROM students 
        JOIN courses ON students.course_id = courses.id
    ''').fetchall()
    conn.close()
    return render_template('index.html', courses=courses, students=students)

@app.route('/add_course', methods=['POST'])
def add_course():
    name = request.form.get('name')
    if name:
        conn = get_db_connection()
        conn.execute('INSERT INTO courses (name) VALUES (?)', (name,))
        conn.commit()
        conn.close()
    return redirect(url_for('index'))

@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form.get('name')
    course_id = request.form.get('course_id')
    if name and course_id:
        conn = get_db_connection()
        conn.execute('INSERT INTO students (name, course_id) VALUES (?, ?)', (name, course_id))
        conn.commit()
        conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
