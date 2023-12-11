import sqlite3


def database():
# Connect to the database 
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

# Create a table to store user information
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT,
            usertype TEXT,
            first_name TEXT,
            last_name TEXT,
            student_id TEXT,
            classification TEXT,
            gpa REAL,
            expected_graduation_date TEXT
            )
    ''')

    conn.commit()
    conn.close()

class User:
    def __init__(self, user_id, username, password, usertype, first_name=None, last_name=None, student_id=None, classification=None, gpa=None, expected_graduation_date=None):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.usertype = usertype
        self.first_name = first_name
        self.last_name = last_name
        self.student_id = student_id
        self.classification = classification
        self.gpa = gpa
        self.expected_graduation_date = expected_graduation_date

class Student(User):
    pass

class Admin(User):
    pass



def login(conn,username, password, usertype):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM users 
        WHERE username = ? AND password = ? AND usertype = ?
    ''', (username, password, usertype))
    
    user_data = cursor.fetchone()

    if user_data:
        # Now unpack all values from user_data
        user_id, username, password, usertype, first_name, last_name, student_id, classification, gpa, expected_graduation_date = user_data
        if usertype.lower() == 'student':
            return Student(user_id, username, password, usertype, first_name, last_name, student_id, classification, gpa, expected_graduation_date)
        elif usertype.lower() == 'admin':
            return Admin(user_id, username, password, usertype)
    return None


def sign_up(conn, username, password, usertype):
    cursor = conn.cursor()
    if usertype.lower() == 'admin':
        cursor.execute('''
            INSERT INTO users (username, password, usertype) VALUES (?, ?, ?)
        ''', (username, password, usertype))
    elif usertype.lower() == 'student':
        first_name = input("Enter your first name: ")
        last_name = input("Enter your last name: ")
        student_id = input("Enter your student ID (in the format @XXXXXXXX): ")
        classification = input("Enter your classification: ")
        gpa = float(input("Enter your current GPA: "))
        expected_graduation_date = input("Enter your expected graduation date (YYYY-MM-DD): ")
        
        cursor.execute('''
            INSERT INTO users (username, password, usertype, first_name, last_name, student_id, classification, gpa, expected_graduation_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (username, password, usertype, first_name, last_name, student_id, classification, gpa, expected_graduation_date))

    conn.commit()
    conn.close()
    print(f"New {usertype} created - Username: {username}, Password: {password}")

def main():

    #Basic terminal prompts to test code , will later be implemented with the front end
    while True:
        print("1. Log in as student")
        print("2. Log in as admin")
        print("3. Sign up")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            student = login(username, password, 'student')
            if student:
                print(f"Welcome, {student.username}!")
                print("Student dashboard is loading...")

                #  Call the student dashboard function here

                # Exit the loop 
                break

            else:
                print("Invalid username or password.")

        elif choice == "2":
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            admin = login(username, password, 'admin')
            if admin:
                print(f"Welcome, {admin.username}!")
                print("Admin dashboard is loading...")
                 # Call the admin dashboard function here

                # Exit the loop 
                break
            else:
                print("Invalid username or password.")

        elif choice == "3":
            username = input("Enter your desired username: ")
            password = input("Enter your desired password: ")
            usertype = input("Are you a student or admin? ").lower()
            sign_up(username, password, usertype)

        elif choice == "4":
            print("Exiting program. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a valid option.")

