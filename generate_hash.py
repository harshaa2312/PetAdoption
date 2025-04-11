import sqlite3
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

conn = sqlite3.connect("instance/user.db")
cursor = conn.cursor()

# Fetch all users with plain text passwords
cursor.execute("SELECT email, password FROM users")
users = cursor.fetchall()

for email, plain_password in users:
    hashed_password = bcrypt.generate_password_hash(plain_password).decode("utf-8")
    cursor.execute("UPDATE users SET password = ? WHERE email = ?", (hashed_password, email))

conn.commit()
conn.close()

print("Passwords updated successfully.")
