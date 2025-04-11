import sqlite3

conn = sqlite3.connect("instance/user.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS adoption_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_email TEXT NOT NULL,
    pet_id INTEGER NOT NULL,
    status TEXT DEFAULT 'Pending',
    FOREIGN KEY(pet_id) REFERENCES pets(id)
)
''')

conn.commit()
conn.close()
print("Adoption Requests table created!")
