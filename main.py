import sqlite3
import hashlib

# Create a SQLite database and connect to it
conn = sqlite3.connect('railway_reservation.db')
cursor = conn.cursor()

# Create User table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS User (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        email TEXT NOT NULL
    )
''')
conn.commit()

# Create Train table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Train (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        train_name TEXT NOT NULL,
        route TEXT NOT NULL,
        departure_time TEXT NOT NULL,
        arrival_time TEXT NOT NULL
    )
''')
conn.commit()

# Create Ticket table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Ticket (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        train_id INTEGER,
        seat_number TEXT NOT NULL,
        booking_date TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES User(id),
        FOREIGN KEY (train_id) REFERENCES Train(id)
    )
''')
conn.commit()

# Helper function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Signup function
def signup():
    print("Signup")
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    email = input("Enter your email: ")

    # Hash the password before storing it
    hashed_password = hash_password(password)

    cursor.execute("INSERT INTO User (username, password, email) VALUES (?, ?, ?)",
                   (username, hashed_password, email))
    conn.commit()
    print("Signup successful.")

# Login function
def login():
    print("Login")
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    hashed_password = hash_password(password)

    cursor.execute("SELECT id FROM User WHERE username = ? AND password = ?", (username, hashed_password))
    user = cursor.fetchone()

    if user:
        print("Login successful.")
    else:
        print("Invalid username or password.")

# Main loop
while True:
    print("\nRailway Reservation System")
    print("1. Signup")
    print("2. Login")
    print("3. Exit")
    choice = input("Enter your choice: ")

    if choice == '1':
        signup()
    elif choice == '2':
        login()
    elif choice == '3':
        print("Goodbye!")
        conn.close()
        break
    else:
        print("Invalid choice. Please try again.")
