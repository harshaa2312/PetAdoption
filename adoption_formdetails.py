import sqlite3

conn = sqlite3.connect("instance/user.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS adoption_form_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_email TEXT NOT NULL,
    pet_id INTEGER NOT NULL,
    name TEXT,
    address TEXT,
    phone TEXT,
    reason TEXT
)
""")

conn.commit()
conn.close()    
print("Adoption form details table created!")
