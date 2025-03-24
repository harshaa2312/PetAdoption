from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Database Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# User Model
class User(db.Model):
    email = db.Column(db.String(100), primary_key=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # Hashed passwords
    role = db.Column(db.String(10), nullable=False)  # "user" or "admin"

# Ensure tables exist and create admin user
with app.app_context():
    db.create_all()  # Create tables if they don’t exist

    # Remove old admin (if any)
    existing_admin = User.query.filter_by(email="admin@gmail.com").first()
    if existing_admin:
        db.session.delete(existing_admin)
        db.session.commit()

    # Insert new admin user with hashed password
    admin_password_hashed = generate_password_hash("123", method="pbkdf2:sha256")
    admin = User(email="admin@gmail.com", password=admin_password_hashed, role="admin")
    db.session.add(admin)
    db.session.commit()

# Home Route
@app.route("/")
def home():
    return render_template("login.html")

# Login Route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        
        user = User.query.filter_by(email=email).first()  # Get user by email

        if user and check_password_hash(user.password, password):  # Validate password correctly
            session["email"] = user.email
            session["role"] = user.role
            return redirect(url_for("dashboard"))

        return "Invalid credentials, try again."

    return render_template("login.html")

# Dashboard Route
@app.route("/dashboard")
def dashboard():
    if "email" in session:
        user_role = session["role"].capitalize()  # Capitalize role (Admin, User)
        return f"Welcome Admin! Role: {user_role}"
    return redirect(url_for("login"))

# Logout Route
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)

