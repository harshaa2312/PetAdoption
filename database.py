import sqlite3

# Connect to SQLite database (or create it if it doesn’t exist)
conn = sqlite3.connect('pet_adoption.db')
cursor = conn.cursor()

# Create Users Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS user (
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL
)
''')
conn.commit()
conn.close()
print("Database setup complete!")