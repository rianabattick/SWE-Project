#main.py
from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulate a database with an in-memory list
academic_records = []

@app.route('/add-class', methods=['POST'])
def add_class():
    class_data = request.json
    academic_records.append(class_data)
    # In a real application, you would save to a database here
    return jsonify(class_data), 200

if __name__ == '__main__':
    app.run(debug=True)