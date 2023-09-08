import sqlite3
import hashlib
import random
import string
import datetime

# Create a SQLite database and connect to it
conn = sqlite3.connect('railway_reservation.db')
cursor = conn.cursor()

# ... (Existing code for creating tables)

# Create TicketBooking table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS TicketBooking (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        train_id INTEGER,
        seat_number TEXT NOT NULL,
        booking_date TEXT NOT NULL,
        ticket_number TEXT NOT NULL,
        payment_amount REAL NOT NULL,
        departure_time TEXT NOT NULL,
        arrival_time TEXT NOT NULL,
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

# Function to generate a random ticket number
def generate_ticket_number():
    ticket_chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(ticket_chars) for _ in range(8))

# Function to book a ticket
def book_ticket():
    print("Book Ticket")
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    # Check if the user is valid
    hashed_password = hash_password(password)
    cursor.execute("SELECT id FROM User WHERE username = ? AND password = ?", (username, hashed_password))
    user = cursor.fetchone()
    
    if user:
        user_id = user[0]
        train_id = int(input("Enter the train ID: "))
        seat_number = input("Enter the seat number: ")
        
        # Get the current date and time
        booking_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Generate a random ticket number
        ticket_number = generate_ticket_number()
        
        # Simulate payment amount (you can implement payment logic here)
        payment_amount = 50.0  # Replace with actual payment logic
        
        # Get departure and arrival times from the Train table (you can fetch these from your Train table)
        cursor.execute("SELECT departure_time, arrival_time FROM Train WHERE id = ?", (train_id,))
        result = cursor.fetchone()
        if result:
            departure_time, arrival_time = result
        else:
            print("Train not found.")
            return
    
        cursor.execute("INSERT INTO TicketBooking (user_id, train_id, seat_number, booking_date, ticket_number, payment_amount, departure_time, arrival_time) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                       (user_id, train_id, seat_number, booking_date, ticket_number, payment_amount, departure_time, arrival_time))
        conn.commit()
        print(f"Ticket booked successfully. Ticket Number: {ticket_number}")
    else:
        print("Invalid username or password.")

# Main loop
while True:
    print("\nRailway Reservation System")
    print("1. Signup")
    print("2. Login")
    print("3. Book Ticket")
    print("4. Exit")
    choice = input("Enter your choice: ")

    if choice == '1':
        signup()
    elif choice == '2':
        login()
    elif choice == '3':
        book_ticket()
    elif choice == '4':
        print("Goodbye!")
        conn.close()
        break
    else:
        print("Invalid choice. Please try again.")
