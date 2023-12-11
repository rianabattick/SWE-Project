from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/student/<int:user_id>')
def display_student_profile(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT first_name, last_name, classification, expected_graduation_date, student_id, gpa
        FROM users 
        WHERE id = ?
    ''', (user_id,))
    student_data = cursor.fetchone()
    conn.close()

    if student_data:
        # Convert the response to a dictionary to jsonify it
        student_profile = {
            "full_name": f"{student_data['first_name']} {student_data['last_name']}",
            "classification": student_data['classification'],
            "expected_graduation_date": student_data['expected_graduation_date'],
            "student_id": student_data['student_id'],
            "gpa": student_data['gpa']
        }
        return jsonify(student_profile)
    else:
        return jsonify({"error": "Student not found"}), 404

@app.route('/update_student_info', methods=['POST'])
def update_student_info():
    # Get data from the form
    classification = request.form['classification']
    graduation = request.form['graduation']
    student_id = request.form['studentId']
    gpa = request.form['gpa']

    # Update the database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE users SET classification=?, expected_graduation_date=?, gpa=? 
        WHERE student_id=?
    ''', (classification, graduation, gpa, student_id))
    conn.commit()
    conn.close()

    # Fetch the updated info to return
    return display_student_profile(user_id=student_id)