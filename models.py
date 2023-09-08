import sqlite3
import hashlib

# Connect to the SQLite database
conn = sqlite3.connect('railway_reservation.db')
cursor = conn.cursor()

# Define the User model
class User:
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def save(self):
        # Hash the password before saving it
        hashed_password = hash_password(self.password)

        cursor.execute("INSERT INTO User (username, password, email) VALUES (?, ?, ?)",
                       (self.username, hashed_password, self.email))
        conn.commit()

    @classmethod
    def login(cls, username, password):
        # Hash the provided password
        hashed_password = hash_password(password)

        cursor.execute("SELECT id FROM User WHERE username = ? AND password = ?", (username, hashed_password))
        user = cursor.fetchone()

        if user:
            return cls(username, password, "")  # Return a User instance if login is successful
        else:
            return None

# Define the Train model
class Train:
    def __init__(self, train_name, route, departure_time, arrival_time):
        self.train_name = train_name
        self.route = route
        self.departure_time = departure_time
        self.arrival_time = arrival_time

    def save(self):
        cursor.execute("INSERT INTO Train (train_name, route, departure_time, arrival_time) VALUES (?, ?, ?, ?)",
                       (self.train_name, self.route, self.departure_time, self.arrival_time))
        conn.commit()

# Define the Ticket model
class Ticket:
    def __init__(self, user_id, train_id, seat_number, booking_date):
        self.user_id = user_id
        self.train_id = train_id
        self.seat_number = seat_number
        self.booking_date = booking_date

    def save(self):
        cursor.execute("INSERT INTO Ticket (user_id, train_id, seat_number, booking_date) VALUES (?, ?, ?, ?)",
                       (self.user_id, self.train_id, self.seat_number, self.booking_date))
        conn.commit()

# Helper function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
