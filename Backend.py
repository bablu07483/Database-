from flask import Flask, render_template, request, redirect
import mysql.connector
from datetime import date

app = Flask(__name__)

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="yourpassword",
    database="attendance_db"
)
cursor = db.cursor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        cursor.execute("INSERT INTO students (name) VALUES (%s)", (name,))
        db.commit()
        return redirect('/')
    return render_template('add_student.html')

@app.route('/mark_attendance', methods=['GET', 'POST'])
def mark_attendance():
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    if request.method == 'POST':
        for student in students:
            status = request.form.get(str(student[0]))
            cursor.execute("INSERT INTO attendance (student_id, date, status) VALUES (%s, %s, %s)",
                           (student[0], date.today(), status))
        db.commit()
        return redirect('/')
    return render_template('mark_attendance.html', students=students)

@app.route('/view_attendance')
def view_attendance():
    cursor.execute("""
        SELECT students.name, attendance.date, attendance.status
        FROM attendance
        JOIN students ON attendance.student_id = students.id
        ORDER BY attendance.date DESC
    """)
    records = cursor.fetchall()
    return render_template('view_attendance.html', records=records)

if __name__ == '__main__':
    app.run(debug=True)

