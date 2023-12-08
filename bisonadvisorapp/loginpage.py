import sqlite3

# Connect to the database 
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create a table to store user information
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT,
        usertype TEXT
    )
''')
conn.commit()

class User:
    def __init__(self, user_id, username, password, usertype):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.usertype = usertype

class Student(User):
    pass

class Admin(User):
    pass

def login(username, password, usertype):
    # Logic to check if the username, password, and usertype match a user record
    cursor.execute('''
        SELECT * FROM users WHERE username = ? AND password = ? AND usertype = ?
    ''', (username, password, usertype))
    
    user_data = cursor.fetchone()

    if user_data:
        user_id, username, password, usertype = user_data
        if usertype.lower() == 'student':
            return Student(user_id, username, password, usertype)
        elif usertype.lower() == 'admin':
            return Admin(user_id, username, password, usertype)

    return None

def sign_up(username, password, usertype):
    # Logic to create a new user and add to the database
    cursor.execute('''
        INSERT INTO users (username, password, usertype) VALUES (?, ?, ?)
    ''', (username, password, usertype))
    conn.commit()

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

if __name__ == "__main__":
    main()

# Close the database connection when done
conn.close()
