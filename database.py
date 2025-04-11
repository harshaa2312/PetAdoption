import sqlite3

# Connect to SQLite database (it will be created if not exists)
conn = sqlite3.connect("instance/user.db")
cursor = conn.cursor()

# Create users table without an ID column
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT CHECK(role IN ('admin', 'user')) NOT NULL
    )
''')

# Check if admin exists, if not, create it
cursor.execute("SELECT * FROM users WHERE email = 'admin@gmail.com'")
admin_exists = cursor.fetchone()

if not admin_exists:
    cursor.execute("INSERT INTO users (email, password, role) VALUES (?, ?, ?)", 
                   ('admin@gmail.com', '123', 'admin'))
    print("Admin account created.")

# Commit and close
conn.commit()
conn.close()
print("Database setup completed successfully.")
