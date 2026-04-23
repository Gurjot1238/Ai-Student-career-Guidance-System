from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import joblib

app = Flask(__name__)
app.secret_key = "mysecretkey"

# Load ML model files
model = joblib.load("career_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")


def get_db_connection():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT UNIQUE,
                password TEXT,
                branch TEXT,
                semester TEXT,
                cgpa TEXT,
                skills TEXT,
                subjects TEXT,
                goals TEXT,
                interests TEXT,
                profile_image TEXT
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS saved_careers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_email TEXT,
                career_name TEXT,
                entered_text TEXT,
                confidence TEXT
            )
        """)
        conn.commit()

    # Maintain your original column update logic
    add_column_if_not_exists("branch", "TEXT")
    add_column_if_not_exists("semester", "TEXT")
    add_column_if_not_exists("cgpa", "TEXT")
    add_column_if_not_exists("skills", "TEXT")
    add_column_if_not_exists("subjects", "TEXT")
    add_column_if_not_exists("goals", "TEXT")
    add_column_if_not_exists("interests", "TEXT")
    add_column_if_not_exists("profile_image", "TEXT")


def add_column_if_not_exists(column_name, column_type):
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("PRAGMA table_info(users)")
        columns = [row["name"] for row in cur.fetchall()]
        if column_name not in columns:
            cur.execute(f"ALTER TABLE users ADD COLUMN {column_name} {column_type}")
            conn.commit()


@app.route("/")
def home():
    if "user_email" in session:
        return redirect(url_for("dashboard"))
    return render_template("login.html")


@app.route("/login.html")
def login_page():
    if "user_email" in session:
        return redirect(url_for("dashboard"))
    return render_template("login.html")


@app.route("/signup.html")
def signup_page():
    return render_template("register.html")

@app.route("/save_user", methods=["POST"])
def save_user():
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]

    try:
        with get_db_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                (name, email, password)
            )
            conn.commit()
        # This line now sends the user directly to the login page
        return redirect(url_for("login_page"))
        
    except sqlite3.IntegrityError:
        # If the email is a duplicate, we keep them here to show the error
        return render_template("register.html", error="User already exists")

@app.route("/login_user", methods=["POST"])
def login_user():
    email = request.form["email"]
    password = request.form["password"]

    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM users WHERE email = ? AND password = ?",
            (email, password)
        )
        user = cur.fetchone()

    if user:
        session["user_email"] = email
        return redirect(url_for("dashboard"))
    else:
        return render_template("login.html", error="Invalid Email or Password")


@app.route("/dashboard")
def dashboard():
    if "user_email" not in session:
        return redirect(url_for("login_page"))

    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = ?", (session["user_email"],))
        user = cur.fetchone()

    return render_template("index.html", user=user)


@app.route("/profile")
def profile():
    if "user_email" not in session:
        return redirect(url_for("login_page"))

    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = ?", (session["user_email"],))
        user = cur.fetchone()

    return render_template("profile.html", user=user)


@app.route("/edit_profile")
def edit_profile():
    if "user_email" not in session:
        return redirect(url_for("login_page"))

    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = ?", (session["user_email"],))
        user = cur.fetchone()

    return render_template("edit_profile.html", user=user)


@app.route("/save_profile", methods=["POST"])
def save_profile():
    if "user_email" not in session:
        return redirect(url_for("login_page"))

    name = request.form["name"]
    branch = request.form["branch"]
    semester = request.form["semester"]
    cgpa = request.form["cgpa"]
    skills = request.form["skills"]
    subjects = request.form["subjects"]
    goals = request.form["goals"]
    interests = request.form["interests"]
    profile_image = request.form["profile_image"]

    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            UPDATE users
            SET name = ?, branch = ?, semester = ?, cgpa = ?, skills = ?,
                subjects = ?, goals = ?, interests = ?, profile_image = ?
            WHERE email = ?
        """, (
            name, branch, semester, cgpa, skills,
            subjects, goals, interests, profile_image,
            session["user_email"]
        ))
        conn.commit()

    return redirect(url_for("profile"))

@app.route("/job_trends")
def job_trends():
    # This will show up in your terminal to prove the route is working
    print(">>> Job Trends route accessed!") 

    if "user_email" not in session:
        print(">>> No session found, redirecting to login.")
        return redirect(url_for("login_page"))

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = ?", (session["user_email"],))
        user = cur.fetchone()
        conn.close()
    except Exception as e:
        print(f">>> Database Error: {e}")
        user = None

    trending_jobs = [
        {"industry": "Artificial Intelligence", "title": "AI Engineer", "min_salary": "10,00,000", "max_salary": "25,00,000+", "growth_percent": 35},
        {"industry": "Data", "title": "Data Scientist", "min_salary": "8,00,000", "max_salary": "20,00,000", "growth_percent": 25},
        {"industry": "Cybersecurity", "title": "Cyber Security Analyst", "min_salary": "6,00,000", "max_salary": "18,00,000", "growth_percent": 28},
        {"industry": "Cloud Computing", "title": "Cloud Engineer", "min_salary": "7,00,000", "max_salary": "22,00,000", "growth_percent": 24},
        {"industry": "Software Engineering", "title": "Software Developer", "min_salary": "5,00,000", "max_salary": "15,00,000", "growth_percent": 12},
        {"industry": "Data", "title": "Data Analyst", "min_salary": "4,00,000", "max_salary": "10,00,000", "growth_percent": 18},
        {"industry": "Web Development", "title": "Web Developer", "min_salary": "3,00,000", "max_salary": "10,00,000", "growth_percent": 10},
        {"industry": "Mobile Development", "title": "App Developer", "min_salary": "4,00,000", "max_salary": "12,00,000", "growth_percent": 15},
        {"industry": "Design", "title": "UI/UX Designer", "min_salary": "4,00,000", "max_salary": "14,00,000", "growth_percent": 14},
        {"industry": "Database Management", "title": "Database Administrator", "min_salary": "5,00,000", "max_salary": "12,00,000", "growth_percent": 8},
        {"industry": "Management", "title": "Project Manager", "min_salary": "10,00,000", "max_salary": "25,00,000", "growth_percent": 9},
        {"industry": "Networking", "title": "Network Engineer", "min_salary": "3,00,000", "max_salary": "9,00,000", "growth_percent": 6}
    ]

    return render_template("job_trends.html", user=user, trending_jobs=trending_jobs)
    
@app.route("/career_assessment")
def career_assessment():
    if "user_email" not in session:
        return redirect(url_for("login_page"))

    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = ?", (session["user_email"],))
        user = cur.fetchone()

    return render_template("career_assessment.html", user=user)


@app.route("/predict", methods=["POST"])
def predict():
    if "user_email" not in session:
        return redirect(url_for("login_page"))

    name_user = request.form["name_user"]
    skills_text = request.form["skills_text"]

    text_vector = vectorizer.transform([skills_text])
    prediction = model.predict(text_vector)[0]

    probabilities = model.predict_proba(text_vector)[0]
    classes = model.classes_
    top_indices = probabilities.argsort()[-3:][::-1]

    top_3 = []
    for i in top_indices:
        top_3.append({
            "career": classes[i],
            "confidence": round(probabilities[i] * 100, 2)
        })

    top_confidence = round(max(probabilities) * 100, 2)

    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = ?", (session["user_email"],))
        user = cur.fetchone()

    return render_template(
        "result.html",
        user=user,
        name=name_user,
        entered_text=skills_text,
        prediction=prediction,
        top_3=top_3,
        top_confidence=top_confidence
    )


@app.route("/save_career", methods=["POST"])
def save_career():
    if "user_email" not in session:
        return redirect(url_for("login_page"))

    career_name = request.form["career_name"]
    entered_text = request.form["entered_text"]
    confidence = request.form["confidence"]

    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO saved_careers (user_email, career_name, entered_text, confidence)
            VALUES (?, ?, ?, ?)
        """, (
            session["user_email"],
            career_name,
            entered_text,
            confidence
        ))
        conn.commit()

    return redirect(url_for("saved_careers"))


@app.route("/saved_careers")
def saved_careers():
    if "user_email" not in session:
        return redirect(url_for("login_page"))

    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = ?", (session["user_email"],))
        user = cur.fetchone()

        cur.execute("""
            SELECT * FROM saved_careers
            WHERE user_email = ?
            ORDER BY id DESC
        """, (session["user_email"],))
        careers = cur.fetchall()

    return render_template("saved_careers.html", user=user, careers=careers)


@app.route("/delete_saved_career/<int:career_id>", methods=["POST"])
def delete_saved_career(career_id):
    if "user_email" not in session:
        return redirect(url_for("login_page"))

    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            DELETE FROM saved_careers
            WHERE id = ? AND user_email = ?
        """, (career_id, session["user_email"]))
        conn.commit()

    return redirect(url_for("saved_careers"))


@app.route("/logout")
def logout():
    session.pop("user_email", None)
    return redirect(url_for("login_page"))


if __name__ == "__main__":
    init_db()
    # Change debug to True and remove use_reloader=False
    app.run(debug=True)