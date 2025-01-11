import sqlite3

# Initialize the database and create the 'listings' table if it doesn't exist
def initialize_db():
    try:
        connection = sqlite3.connect("db.sqlite")
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS listings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                location TEXT NOT NULL,
                budget INTEGER NOT NULL,
                amenities TEXT,
                contact TEXT NOT NULL
            );
        ''')
        connection.commit()
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        connection.close()

# Function to add a listing to the database
def add_listing(name, location, budget, amenities, contact):
    try:
        connection = sqlite3.connect("db.sqlite")
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO listings (name, location, budget, amenities, contact)
            VALUES (?, ?, ?, ?, ?);
        ''', (name, location, budget, amenities, contact))
        connection.commit()
    except Exception as e:
        print(f"Error adding listing: {e}")
    finally:
        connection.close()

# Function to retrieve listings with optional filters for budget and location
def get_listings(filter_budget=None, filter_location=None):
    try:
        connection = sqlite3.connect("db.sqlite")
        cursor = connection.cursor()

        query = 'SELECT id, name, location, budget, amenities, contact FROM listings WHERE 1=1'
        params = []

        if filter_budget is not None:
            query += ' AND budget <= ?'
            params.append(filter_budget)

        if filter_location:
            query += ' AND location LIKE ?'
            params.append(f"%{filter_location}%")

        cursor.execute(query, params)
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        print(f"Error fetching listings: {e}")
        return []
    finally:
        connection.close()
