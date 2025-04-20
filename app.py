from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3
import os  
from flask import Flask, render_template, request, redirect, url_for, session
from flask import flash
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename 
app = Flask(__name__)
app.secret_key = "your_secret_key"
bcrypt = Bcrypt(app)

UPLOAD_FOLDER = os.path.join("static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Function to connect to the database
def get_db_connection():
    conn = sqlite3.connect("instance/user.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"].lower()

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()

        if user and bcrypt.check_password_hash(user["password"], password) and user["role"].lower() == role:
            session["email"] = email
            session["role"] = role
            return redirect("/admin_dashboard" if role == "admin" else "/user_dashboard")
        else:
            return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")

@app.route("/register", methods=["POST"])
def register():
    email = request.form["email"]
    password = request.form["password"]
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    role = "user"

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (email, password, role) VALUES (?, ?, ?)", 
                       (email, hashed_password, role))
        conn.commit()
        conn.close()
        return jsonify({"status": "success"})
    except sqlite3.IntegrityError:
        return jsonify({"status": "error", "message": "Email already registered"})

@app.route("/admin_dashboard")
def admin_dashboard():
    if session.get("role") != "admin":
        return redirect("/")
    return render_template("admin_dashboard.html", email=session["email"])

@app.route("/user_dashboard")
def user_dashboard():
    if session.get("role") != "user":
        return redirect("/")
    return render_template("user_dashboard.html", email=session["email"])

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# 🔥 Updated with image upload support
@app.route("/manage_pets", methods=["GET", "POST"])
def manage_pets():
    if session.get("role") != "admin":
        return redirect("/")

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        name = request.form["name"]
        breed = request.form["breed"]
        age = request.form["age"]
        image_file = request.files.get("image")
        image_path = None

        if image_file and image_file.filename != "":
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            image_file.save(image_path)

        cursor.execute("INSERT INTO pets (name, breed, age, status, image) VALUES (?, ?, ?, 'Available', ?)",
                       (name, breed, age, image_path))
        conn.commit()

    cursor.execute("SELECT * FROM pets")
    pets = cursor.fetchall()
    conn.close()

    return render_template("manage_pets.html", pets=pets)
@app.route('/add_pet', methods=['POST'])
def add_pet():
    name = request.form['name']
    breed = request.form['breed']
    age = request.form['age']
    image = request.files['image']

    filename = None
    if image and image.filename != '':
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    conn = sqlite3.connect('instance/user.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO pets (name, breed, age, image) VALUES (?, ?, ?, ?)',
                   (name, breed, age, filename))
    conn.commit()
    conn.close()

    flash('Pet added successfully!', 'success')
    return redirect(url_for('manage_pets'))
@app.route('/delete_pet/<int:pet_id>', methods=['GET'])
def delete_pet(pet_id):
    conn = sqlite3.connect('instance/user.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM pets WHERE id = ?', (pet_id,))
    conn.commit()
    conn.close()
    flash('Pet deleted successfully!', 'success')
    return redirect(url_for('manage_pets'))


# Edit Pet - Show form and update pet
@app.route('/edit_pet/<int:pet_id>', methods=['GET', 'POST'])
def edit_pet(pet_id):
    conn = sqlite3.connect('instance/user.db')
    c = conn.cursor()

    if request.method == 'POST':
        # Get updated data from form
        name = request.form['name']
        breed = request.form['breed']
        age = request.form['age']
        image_file = request.files['image']

        # If user uploaded a new image
        if image_file and image_file.filename != '':
            image_filename = image_file.filename
            image_path = os.path.join('static/uploads', image_filename)
            image_file.save(image_path)

            # Update all fields including image
            c.execute('UPDATE pets SET name=?, breed=?, age=?, image=? WHERE id=?',
                      (name, breed, age, image_filename, pet_id))
        else:
            # Update without changing the image
            c.execute('UPDATE pets SET name=?, breed=?, age=? WHERE id=?',
                      (name, breed, age, pet_id))

        conn.commit()
        conn.close()
        flash('Pet updated successfully!', 'success')
        return redirect(url_for('manage_pets'))
    else:
        # Fetch pet details to pre-fill the form
        c.execute('SELECT * FROM pets WHERE id=?', (pet_id,))
        pet = c.fetchone()
        conn.close()

        if pet:
            return render_template('edit_pet.html', pet=pet)
        else:
            flash('Pet not found!', 'error')
            return redirect(url_for('manage_pets'))


@app.route("/manage_adoptions")
def manage_adoptions():
    if session.get("role") != "admin":
        return redirect("/")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ar.id, ar.user_email, p.name AS pet_name, ar.status 
        FROM adoption_requests ar
        JOIN pets p ON ar.pet_id = p.id
    """)
    requests = cursor.fetchall()
    conn.close()

    return render_template("manage_adoptions.html", requests=requests)

@app.route("/update_request/<int:request_id>", methods=["POST"])
def update_request(request_id):
    if session.get("role") != "admin":
        return redirect("/")

    new_status = request.form["action"]

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE adoption_requests SET status = ? WHERE id = ?", (new_status, request_id))

    if new_status == "Approved":
        cursor.execute("SELECT pet_id FROM adoption_requests WHERE id = ?", (request_id,))
        pet_id = cursor.fetchone()["pet_id"]
        cursor.execute("UPDATE pets SET status = 'Adopted' WHERE id = ?", (pet_id,))

    conn.commit()
    conn.close()

    return redirect("/manage_adoptions")

@app.route("/adoption_requests")
def adoption_requests():
    if session.get("role") != "admin":
        return redirect("/")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM adoption_requests")
    adoption_requests = cursor.fetchall()
    conn.close()

    return render_template("adoption_requests.html", adoption_requests=adoption_requests)

@app.route("/approve_request/<int:request_id>", methods=["POST"])
def approve_request(request_id):
    if session.get("role") != "admin":
        return redirect("/")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE adoption_requests SET status = 'Approved' WHERE id = ?", (request_id,))
    cursor.execute("SELECT pet_id FROM adoption_requests WHERE id = ?", (request_id,))
    pet_id = cursor.fetchone()["pet_id"]
    cursor.execute("UPDATE pets SET status = 'Adopted' WHERE id = ?", (pet_id,))
    conn.commit()
    conn.close()

    return redirect("/adoption_requests")

@app.route("/reject_request/<int:request_id>", methods=["POST"])
def reject_request(request_id):
    if session.get("role") != "admin":
        return redirect("/")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE adoption_requests SET status = 'Rejected' WHERE id = ?", (request_id,))
    conn.commit()
    conn.close()

    return redirect("/adoption_requests")

@app.route("/available_pets", methods=["GET"])
def available_pets():
    if session.get("role") != "user":
        return redirect("/")

    search_query = request.args.get("search", "").lower()

    conn = get_db_connection()
    cursor = conn.cursor()

    if search_query:
        cursor.execute("SELECT * FROM pets WHERE LOWER(breed) LIKE ? AND status = 'Available'", 
                       ('%' + search_query + '%',))
    else:
        cursor.execute("SELECT * FROM pets WHERE status = 'Available'")

    pets = cursor.fetchall()
    conn.close()

    return render_template("available_pets.html", pets=pets, search_query=search_query)
@app.route("/adopt/<int:pet_id>", methods=["GET", "POST"])
def adopt_pet(pet_id):
    if session.get("role") != "user":
        return redirect("/")

    if request.method == "POST":
        user_email = session.get("email")
        status = "Pending"
        conn = sqlite3.connect("instance/user.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO adoption_requests (user_email, pet_id, status) VALUES (?, ?, ?)",
                       (user_email, pet_id, status))
        conn.commit()
        conn.close()
        return redirect("/user_dashboard")

    return render_template("adopt_form.html", pet_id=pet_id)
@app.route('/submit_adoption/<int:pet_id>', methods=['POST'])
def submit_adoption_form(pet_id):

    if session.get("role") != "user":
        return redirect("/")

    user_email = session.get("email")
    name = request.form["name"]
    email = request.form["email"]
    address = request.form["address"]
    phone = request.form["phone"]
    reason = request.form["reason"]

    conn = get_db_connection()
    cursor = conn.cursor()

    # Insert into adoption_requests
    cursor.execute("INSERT INTO adoption_requests (user_email, pet_id, status) VALUES (?, ?, ?)",
                   (user_email, pet_id, "Pending"))

    # Insert into adoption_form_details
    cursor.execute("""
        INSERT INTO adoption_form_details (user_email, pet_id, name, address, phone, reason)
        VALUES (?, ?, ?, ?, ?, ?)""",
        (user_email, pet_id, name, address, phone, reason))

    conn.commit()
    conn.close()

    return redirect(url_for("user_dashboard"))



@app.route("/submit_adoption_request/<int:pet_id>", methods=["POST"])
def submit_adoption_request(pet_id):
    user_email = session["email"]
    conn = sqlite3.connect("instance/user.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO adoption_requests (user_email, pet_id, status) VALUES (?, ?, ?)",
                   (user_email, pet_id, "Pending"))
    conn.commit()
    conn.close()
    return redirect(url_for("manage_adoptions"))

@app.route('/admin/adoption_requests')
def admin_adoption_requests():
    conn = sqlite3.connect('instance/user.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM adoption_requests')
    requests = cursor.fetchall()
    conn.close()
    return render_template('admin_adoption_requests.html', requests=requests)
@app.route('/admin/pet/<int:pet_id>')
def view_pet_details(pet_id):
    conn = sqlite3.connect('instance/user.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pets WHERE id = ?", (pet_id,))
    pet = cursor.fetchone()
    conn.close()
    return render_template('view_pet_details.html', pet=pet)
@app.route("/admin/view_adoption_form/<user_email>/<int:pet_id>")
def view_adoption_form(user_email, pet_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM adoption_form_details 
        WHERE user_email = ? AND pet_id = ?
    """, (user_email, pet_id))
    
    form = cursor.fetchone()
    conn.close()

    if form:
        return render_template("view_adoption_form.html", form=form)
    else:
        flash("Form not found.")
        return redirect(url_for("manage_adoption_requests"))

@app.route('/view_adoption_request/<int:request_id>')
def view_adoption_request(request_id):
    conn = sqlite3.connect('instance/user.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Get main request info
    cursor.execute("SELECT * FROM adoption_requests WHERE id = ?", (request_id,))
    request_data = cursor.fetchone()

    if not request_data:
        conn.close()
        return "Request not found", 404

    # Get additional form details
    cursor.execute("""
        SELECT * FROM adoption_form_details 
        WHERE user_email = ? AND pet_id = ?
    """, (request_data["user_email"], request_data["pet_id"]))
    form_data = cursor.fetchone()

    conn.close()

    return render_template('view_adoption_request.html', request_data=request_data, form_data=form_data)



if __name__ == "__main__":
    app.run(debug=True)

