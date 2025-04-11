import sqlite3

conn = sqlite3.connect("instance/user.db")
cursor = conn.cursor()

# Insert a test adoption request (Change pet_id as needed)
cursor.execute("INSERT INTO adoption_requests (user_email, pet_id, status) VALUES (?, ?, ?)",
               ("testuser@example.com", 1, "Pending"))

conn.commit()
conn.close()
print("Test adoption request added!")
