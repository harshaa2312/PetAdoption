import sqlite3

conn = sqlite3.connect("instance/user.db")
cursor = conn.cursor()

# Create pets table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS pets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    breed TEXT NOT NULL,
    age INTEGER NOT NULL,
    status TEXT DEFAULT 'Available' -- Available or Adopted
)
''')

# Check if 'image' column already exists
cursor.execute("PRAGMA table_info(pets)")
columns = [column[1] for column in cursor.fetchall()]

if 'image' not in columns:
    cursor.execute("ALTER TABLE pets ADD COLUMN image TEXT")
    print("Image column added to pets table.")
else:
    print("Image column already exists.")

conn.commit()
conn.close()
print("Pets table setup complete!")
